import { writable, derived } from 'svelte/store';

// Create a store to hold the user details
const userStore = writable(null);

// Create a derived store which will update whenever userStore updates
export const loginStatus = derived(
    userStore,
    $userStore => $userStore ? $userStore.email : 'Not logged in'
);

// Function to update userStore
export function updateUserStore() {
    const userDetails = localStorage.getItem("user_details");
    if(userDetails) {
        const parsedDetails = JSON.parse(userDetails);
        userStore.set(parsedDetails);
    } else {
        userStore.set(null);
    }
}