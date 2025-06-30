import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY, // Server-side only, not exposed to frontend
});

const SYSTEM_PROMPT = `
You are an expert at analyzing bill/receipt images and extracting structured data. 
Analyze the uploaded bill image and extract the following information in JSON format:

{
  "dates": ["list of dates found in the bill"],
  "items": [
    {
      "name": "item name",
      "quantity": "quantity with unit (e.g., '2 kg', '1 adet')",
      "unit_price": "price per unit if available",
      "total_price": "total price for this item",
      "line_text": "original text line where this item was found"
    }
  ],
  "amounts": [
    {
      "value": "numerical value",
      "currency": "currency symbol or code",
      "description": "what this amount represents (e.g., 'subtotal', 'tax', 'total')",
      "original_text": "original text as it appears in the bill"
    }
  ],
  "totals": {
    "subtotal": "subtotal amount if available",
    "tax": "tax amount if available", 
    "total": "final total amount",
    "currency": "currency used"
  },
  "merchant_info": {
    "name": "merchant/store name if visible",
    "address": "address if visible",
    "phone": "phone number if visible"
  },
  "bill_metadata": {
    "bill_number": "receipt/bill number if available",
    "cashier": "cashier name/ID if available",
    "payment_method": "payment method if specified"
  }
}

IMPORTANT INSTRUCTIONS:
1. Extract ALL visible text accurately
2. For Turkish bills, recognize Turkish characters properly (ç, ğ, ı, ö, ş, ü)
3. Parse dates in various formats (DD/MM/YYYY, DD.MM.YYYY, etc.)
4. Identify currency symbols (₺ for Turkish Lira, $ for Dollar, € for Euro)
5. Extract quantities and units (kg, gr, lt, adet, paket, etc.)
6. Calculate totals when possible
7. If information is not available, use null or empty string
8. Be precise with numerical values
9. Preserve original text formatting when possible

Return ONLY the JSON response, no additional text or formatting.
`;

export async function POST(request: NextRequest) {
  try {
    // Check if API key is configured
    if (!process.env.OPENAI_API_KEY) {
      return NextResponse.json(
        { error: 'OpenAI API key not configured' },
        { status: 500 }
      );
    }

    // Parse form data
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      );
    }

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp', 'image/tiff'];
    if (!allowedTypes.includes(file.type)) {
      return NextResponse.json(
        { error: 'Unsupported file type' },
        { status: 400 }
      );
    }

    // Validate file size (10MB limit)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      return NextResponse.json(
        { error: 'File too large (max 10MB)' },
        { status: 400 }
      );
    }

    // Convert file to base64
    const bytes = await file.arrayBuffer();
    const base64 = Buffer.from(bytes).toString('base64');

    // Call OpenAI API
    const response = await client.chat.completions.create({
      model: "gpt-4o",
      messages: [
        {
          role: "system",
          content: SYSTEM_PROMPT
        },
        {
          role: "user",
          content: [
            {
              type: "text",
              text: "Please analyze this bill/receipt image and extract the structured data as requested."
            },
            {
              type: "image_url",
              image_url: {
                url: `data:image/jpeg;base64,${base64}`,
                detail: "high"
              }
            }
          ]
        }
      ],
      max_tokens: 2000,
      temperature: 0.1
    });

    const responseText = response.choices[0].message.content?.trim() || '';
    
    // Parse the JSON response
    let extractedData;
    try {
      // Remove any markdown formatting if present
      let cleanedResponse = responseText;
      if (cleanedResponse.startsWith('```json')) {
        cleanedResponse = cleanedResponse.slice(7);
      }
      if (cleanedResponse.endsWith('```')) {
        cleanedResponse = cleanedResponse.slice(0, -3);
      }
      
      extractedData = JSON.parse(cleanedResponse);
    } catch (parseError) {
      return NextResponse.json({
        success: false,
        error: 'Failed to parse GPT-4o response',
        raw_response: responseText,
        filename: file.name,
        timestamp: new Date().toISOString()
      });
    }

    // Transform to match the expected format
    const result = {
      raw_text: {
        gpt4o_response: responseText,
        combined: responseText
      },
      extracted_data: {
        dates: extractedData.dates || [],
        amounts: (extractedData.amounts || []).map((amt: any) => ({
          original: amt.original_text || '',
          value: String(amt.value || ''),
          position: [0, 0]
        })),
        items: (extractedData.items || []).map((item: any) => ({
          line: item.line_text || '',
          items: [item.name || ''],
          quantities: item.quantity ? [item.quantity] : [],
          amounts: item.total_price ? [{
            original: String(item.total_price),
            value: String(item.total_price),
            position: [0, 0]
          }] : []
        })),
        total_calculated: extractedData.totals?.total ? 
          parseFloat(String(extractedData.totals.total).replace(/[^\d.,]/g, '').replace(',', '.')) : null,
        item_count: extractedData.items?.length || 0,
        merchant_info: extractedData.merchant_info || {},
        bill_metadata: extractedData.bill_metadata || {}
      },
      processing_info: {
        timestamp: new Date().toISOString(),
        method: 'gpt-4o-vision',
        model: 'gpt-4o',
        tokens_used: response.usage?.total_tokens || null,
        preprocessing_applied: false
      }
    };

    return NextResponse.json({
      success: true,
      filename: file.name,
      result: result
    });

  } catch (error) {
    console.error('Error processing bill:', error);
    
    return NextResponse.json(
      { 
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred' 
      },
      { status: 500 }
    );
  }
}
