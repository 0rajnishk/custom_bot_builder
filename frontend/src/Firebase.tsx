import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

// export const app = initializeApp({
//   apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
//   authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
//   databaseURL: process.env.REACT_APP_FIREBASE_DATABASE_URL,
//   projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
//   storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
//   messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
//   appId: process.env.REACT_APP_FIREBASE_APP_ID,
//   measurementId: process.env.REACT_APP_FIREBASE_APP_MEASUREMENT_ID
// })
export const app = initializeApp({
  apiKey: "AIzaSyBNgOPPBm34js9ihyzmOlkt1dMDG4UAmAo",
  authDomain: "chat-buiz.firebaseapp.com",
  projectId: "chat-buiz",
  storageBucket: "chat-buiz.appspot.com",
  messagingSenderId: "102685653236",
  appId: "1:102685653236:web:e1a58b8c00c364971c06a1",
  measurementId: "G-EZ0EC62DB3"
})
// export const APP_COLLECTION = 'users'
export const auth = getAuth(app)
export const firestore = getFirestore(app)
