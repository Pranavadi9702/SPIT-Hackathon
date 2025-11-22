import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCKfoaEPgUht3nvzRE4Nedlc-GCu6AquZA",
  authDomain: "crm-chainforest.firebaseapp.com",
  projectId: "crm-chainforest",
  storageBucket: "crm-chainforest.firebasestorage.app",
  messagingSenderId: "756476157222",
  appId: "1:756476157222:web:977f10bbed7a42629c35e7",
  measurementId: "G-CCKFKKEMX2"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
