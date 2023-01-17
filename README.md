# Commerce - auction site

An eBay-like e-commerce auction site.

The website allows users to post listings on auction, place bids on listings, comment on those listings, and add listings to a watch list. The owner of the auction item can close the auction.

## If the user is not signed in
### Active listings
Allows users to view all of the currently active auction listings. 
Users have options: to see all active listings or active listings by category, to log in (if registered), and to register.

### Log in
Username, password, log in.

### Register
Username, e-mail, password, confirm password, register.

### Listing Page
Clicking on a listing, users can see information specific to that listing, including the current price and comments.

## If the user is signed in
### Active Listings
### Listing Page
Clicking on a listing, users can see all information specific to that listing, including the current price and comments.

The user can add the item to their “Watchlist” or remove it if already there. The user can bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user is presented with an error.

If the user is the owner of the listing, he can “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.

Users who are signed in also can add comments to the listing page. The listing page displays all comments that have been made on the listing.

### Create new listing
Title, Category (Select a category from the dropdown and Select button), Description, Image URL, Price, Save button.

### Watchlist
Add bid, Add comment, Remove from Watchlist button.

### Log out

## Django Admin Interface
Site administrators are able to view, add, edit, and delete users, categories, listings, comments, and bids made on the site. Also, the only way to make a new category is by using Django Admin Interface.