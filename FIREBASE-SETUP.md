# Firebase Setup Guide

## Step 1: Create a Firebase Project

1. Go to [https://console.firebase.google.com](https://console.firebase.google.com)
2. Click **Add project** → name it (e.g. `safwane-wedding`)
3. Disable Google Analytics (not needed)

## Step 2: Add a Web App

1. In your project, click the **Web icon** `</>` (Add app → Web)
2. Name it `wedding-admin`
3. Copy the `firebaseConfig` object — you'll paste it into `admin.html`

## Step 3: Enable Authentication

1. Go to **Build → Authentication → Get started**
2. Enable **Email/Password** sign-in method
3. Go to **Users → Add User**
4. Create your admin account (email + password)

## Step 4: Enable Firestore Database

1. Go to **Build → Firestore Database → Create database**
2. Start in **production mode**
3. Pick a location close to you (e.g. `europe-west1`)

## Step 5: Set Firestore Security Rules

Go to **Firestore → Rules** and paste:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Admin must be authenticated
    function isAdmin() {
      return request.auth != null;
    }
    
    // Wedding config: public read, admin write
    match /wedding/{doc} {
      allow read: if true;
      allow write: if isAdmin();
    }
    
    // RSVPs: anyone can create, only admin can read/delete
    match /rsvp/{doc} {
      allow create: if true;
      allow read, update, delete: if isAdmin();
    }
    
    // Guests: admin only
    match /guests/{doc} {
      allow read, write: if isAdmin();
    }
  }
}
```

## Step 6: Update admin.html

Open `admin.html` and replace the `FIREBASE_CONFIG` object (near line 230) with your actual config:

```js
const FIREBASE_CONFIG = {
  apiKey: "AIza...",         // your actual API key
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "1234567890",
  appId: "1:1234567890:web:abc123"
};
```

## Step 7: Deploy

```bash
git add -A && git commit -m "Admin panel with Firebase" && git push
```

Your admin panel will be live at:
**https://safwaneettih.github.io/wedding/admin.html**

## Firestore Data Structure

```
wedding/
  config/        → single doc with all invitation content

rsvp/            → collection, one doc per RSVP submission
  {auto-id}/
    name, email, attending, message, created_at

guests/          → collection, one doc per guest
  {auto-id}/
    name, email, phone, rsvp_status, created_at
```

## What the admin can do

- **Dashboard**: See stats (total guests, confirmed, declined, pending) + recent RSVPs
- **Content**: Edit couple names, families, dates, events with save to Firestore
- **RSVPs**: View all submissions, filter by attending, export CSV
- **Guests**: Add/remove guests, track RSVP status