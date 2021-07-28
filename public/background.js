// Your web app's Firebase configuration
var firebaseConfig = {
    apiKey: "AIzaSyAw6T0-TjETx7x7giOZQH4HzJurVsVm2IY",
    authDomain: "comments-for--315620.firebaseapp.com",
    projectId: "comments-for-youtube-315620",
    storageBucket: "comments-for-youtube-315620.appspot.com",
    messagingSenderId: "688328849184",
    appId: "1:688328849184:web:693eeec3da713f0b348945",
    measurementId: "G-4NTQRB4M6S",
};

firebase.initializeApp(firebaseConfig);

console.log(firebase);

var provider = new firebase.auth.GoogleAuthProvider();

// EXTENSION ACTIVATION 
chrome.tabs.onUpdated.addListener(function (tabId, info, tab) {
    if (tab.url.startsWith("https://www.youtube.com/watch?v=")) {

        chrome.action.enable(tabId);
    } else {
        chrome.action.disable(tabId);
    }
});

// USER AUTH METHODS
chrome.runtime.onMessage.addListener((msg, sender, response) => {
    if (msg.command == 'logoutAuth') {
        firebase.auth().signOut().then(function () {
            // Sign-out successful.
            response({ type: "un-auth", status: "success", message: true });
        }, function (error) {
            // An error happened.
            response({ type: "un-auth", status: "false", message: error });
        });
    }
    if (msg.command == 'checkAuth') {
        var user = firebase.auth().currentUser;
        if (user) {
            // User is signed in.
            response({ type: "auth", status: "success", message: user });
        } else {
            // No user is signed in.
            response({ type: "auth", status: "no-auth", message: false });
        }
    }
    if (msg.command == 'loginUser') {
        firebase.auth()
            .signInWithPopup(provider)
            .then((result) => {
                /** @type {firebase.auth.OAuthCredential} */
                var credential = result.credential;

                // This gives you a Google Access Token. You can use it to access the Google API.
                var token = credential.accessToken;
                // The signed-in user info.
                var user = result.user;
                // ...
                response({ type: "auth", status: "success", message: user });
            }).catch((error) => {
                // Handle Errors here.
                var errorCode = error.code;
                var errorMessage = error.message;
                // The email of the user's account used.
                var email = error.email;
                // The firebase.auth.AuthCredential type that was used.
                var credential = error.credential;
                // ...
                response({ type: "auth", status: "error", message: errorMessage });
            });

    }

    return true;
});