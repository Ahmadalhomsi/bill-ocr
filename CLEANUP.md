# Files to Remove for Frontend-Only Setup

## 🗑️ Can be safely deleted:

### Directories:
- `backend/` - Entire backend directory (Python FastAPI server)

### Files:
- `setup.bat` - Old setup script for backend
- `setup.sh` - Old setup script for backend
- `start.bat` - Backend startup script
- `test_system.py` - Python test script
- `docker-compose.yml` - Docker configuration
- `Dockerfile.frontend` - Docker configuration
- `.dockerignore` - Docker ignore file

### Keep these:
- `setup-simple.bat` - New simple setup
- `setup-simple.sh` - New simple setup
- `test-system.js` - Frontend test script (can be updated)
- All files in `app/`, `public/`, `node_modules/`
- `package.json`, `tsconfig.json`, etc.

## 🧹 Cleanup Commands:

```bash
# Remove backend directory
rm -rf backend/

# Remove old scripts
rm setup.bat setup.sh start.bat test_system.py

# Remove Docker files
rm docker-compose.yml Dockerfile.frontend .dockerignore

# Rename new setup scripts
mv setup-simple.bat setup.bat
mv setup-simple.sh setup.sh
```

## ✅ What you'll have left:
- Clean Next.js frontend application
- Direct OpenAI API integration
- Simple setup process
- No backend dependencies
- Easy deployment to Vercel/Netlify
