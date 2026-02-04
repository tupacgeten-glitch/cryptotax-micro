# Deployment Guide - CryptoTax Micro

## ✅ Prerequisites Completed
- [x] GitHub repository created
- [x] Vercel account connected to GitHub

## 🚀 Deploy to Vercel (5 minutes)

### Step 1: Import Project
1. Go to https://vercel.com/new
2. Click "Import Git Repository"
3. Select `tupacgeten-glitch/cryptotax-micro`
4. Click "Import"

### Step 2: Configure Build Settings

**Framework Preset:** Next.js

**Root Directory:** `frontend`

**Build Command:** (leave as default)
```
npm run build
```

**Output Directory:** (leave as default)
```
.next
```

**Install Command:** (leave as default)
```
npm install
```

### Step 3: Environment Variables
No environment variables needed for MVP!
(We'll add Stripe keys later in Day 3)

### Step 4: Deploy
1. Click "Deploy"
2. Wait 2-3 minutes for build to complete
3. You'll get a URL like: `cryptotax-micro.vercel.app`

## 🔧 Post-Deployment

### Test the Deployment
1. Visit your Vercel URL
2. Download the sample CSV
3. Upload it and test the calculator
4. Verify results display correctly

### Add Custom Domain (Optional - Day 3)
1. Buy domain (e.g., `simpletaxcrypto.com`)
2. In Vercel dashboard → Settings → Domains
3. Add your domain
4. Follow DNS configuration steps
5. Wait 5-10 minutes for propagation

## ⚠️ Known Issues & Fixes

### Issue: Backend API not working
**Problem:** Python backend needs separate deployment

**Solution:** 
For MVP, we're using mock data in the frontend API routes.
For production (Day 3), we'll deploy the Python backend separately.

### Issue: PDF download not working
**Problem:** PDF generation is backend-only currently

**Fix for Day 3:**
Deploy Python backend to Vercel or Railway, connect to frontend.

## 📊 What Works Right Now (MVP)

✅ Landing page  
✅ File upload interface  
✅ Cost basis method selection  
✅ Sample CSV download  
✅ Mock calculation results display  
⏳ Real tax calculations (needs backend deployment)  
⏳ PDF download (needs backend deployment)  

## 🎯 Next Steps (Your Action Items)

1. **Deploy to Vercel** (5 min)
   - Follow steps above
   - Get live URL

2. **Test the Site** (2 min)
   - Upload sample CSV
   - Verify UI works
   - Check mobile responsiveness

3. **Share the URL** (1 min)
   - Send me the Vercel URL
   - I'll verify deployment
   - We'll plan Day 3 tasks

## 🐛 Troubleshooting

### Build Fails
**Error:** `Module not found`  
**Fix:** Make sure Root Directory is set to `frontend`

### 404 on Homepage
**Error:** Page not found  
**Fix:** Check that `frontend/pages/index.tsx` exists in repo

### Styling Broken
**Error:** No Tailwind CSS  
**Fix:** Verify `tailwind.config.js` and `postcss.config.js` are in root

## 📞 Need Help?

If deployment fails:
1. Check Vercel build logs
2. Screenshot any errors
3. Send me the error message
4. I'll debug and fix

---

## 🎉 Success Checklist

After deployment, you should have:
- [ ] Live URL (e.g., cryptotax-micro.vercel.app)
- [ ] Landing page loads
- [ ] Can upload CSV files
- [ ] Sample CSV downloads
- [ ] UI looks good on mobile
- [ ] No console errors

Once these are checked, we're ready for Day 3:
- Stripe integration
- Real backend deployment
- Domain purchase

**Estimated time:** 5-10 minutes total

---

Ready? Let's deploy! 🚀
