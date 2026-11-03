# Cloudinary Setup for Persistent Image Storage

## Why Cloudinary?

Render's free tier has an **ephemeral filesystem** - uploaded images are deleted when the app restarts or redeploys. Cloudinary stores images permanently in the cloud, so they persist across deployments.

## Step 1: Create Cloudinary Account (Free)

1. Go to https://cloudinary.com
2. Click **"Sign Up"** (free tier available)
3. Sign up with email or Google
4. Verify your email

## Step 2: Get Your Cloudinary Credentials

1. After signing up, go to your **Dashboard**
2. You'll see:
   - **Cloud Name**
   - **API Key**
   - **API Secret**
3. Click **"Copy"** next to **"Environment Variable"** (it looks like: `CLOUDINARY_URL=cloudinary://...`)

## Step 3: Add Environment Variables to Render

1. Go to your **DollHouse** web service in Render Dashboard
2. Click **"Settings"** tab
3. Scroll to **"Environment Variables"**
4. Add this variable:
   - **Key**: `CLOUDINARY_URL`
   - **Value**: Paste the environment variable you copied from Cloudinary
5. Click **"Save Changes"**

## Step 4: Deploy

1. Click **"Manual Deploy"** in Render
2. Select **"Clear build cache & deploy"**
3. Click **"Deploy"**

## What This Does

- All uploaded images (owner photo, salon images, product images) will be stored in Cloudinary
- Images will persist across deployments and app restarts
- All users will see the same images
- Cloudinary free tier: 25GB storage, 25GB bandwidth/month (more than enough)

## Verification

After deployment:
1. Upload an owner photo via admin panel
2. Check that it appears on the homepage
3. Trigger a manual deploy again
4. The image should still be there (not deleted)
