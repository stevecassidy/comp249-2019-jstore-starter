describe('Can load main page', function(){
    it("displays a table of products", function(){
        cy.visit('http://localhost:8010/');

        /* find a table */
        cy.get("table")
        /* look for a product in a <td> and then the price in the next <td> */
        .contains("td", "Ocean Blue Shirt").next().contains("$33");

    });

    it("shows product detail when I click on a product", function(){
        cy.visit('http://localhost:8010/');

        cy.contains('Ocean Blue Shirt').click();
        /* product detail is displayed: description, image, cost */
        cy.contains('Ocean blue cotton shirt');
        cy.get("img[src='https://burst.shopifycdn.com/photos/young-man-in-bright-fashion_925x.jpg']");
        cy.contains("33");
    });

    it("lets me close the product detail", function(){
        cy.visit('http://localhost:8010/');

        cy.contains('Ocean Blue Shirt').click();
        /* we see the product image */
        cy.get("img[src='https://burst.shopifycdn.com/photos/young-man-in-bright-fashion_925x.jpg']");
        /* find the text 'Close' and click it */
        cy.contains("Close").click();
        /* can no longer see the product image */
        cy.get("img[src='https://burst.shopifycdn.com/photos/young-man-in-bright-fashion_925x.jpg']")
        .should('not.be.visible');
    });

    it("has an add to cart form when I click on a product", function(){
        cy.visit('http://localhost:8010/');

        cy.contains('Ocean Blue Shirt').click();
        cy.contains('form').get('input[name=productid]').should('have.value', '0');
        cy.contains('form').get('input[name=quantity]');
    });

    it("adds products to the cart when I submit the form", function(){
        cy.visit('http://localhost:8010/');

        /* initial page contains $0.00 - initial total for shopping cart */
        cy.contains('$0.00');
        cy.contains('Ocean Blue Shirt').click();
        cy.contains('form').get('input[name=productid]').should('have.value', '0');
        cy.contains('form').get('input[name=quantity]').clear().type(3);
        cy.get('form').submit();
        /* we see the cart total updated */
        cy.contains('$99');

        /* add a second product */
        cy.contains('Black Leather Bag').click();
        cy.contains('form').get('input[name=productid]').should('have.value', '9');
        cy.contains('form').get('input[name=quantity]').clear().type(1);
        cy.get('form').submit();
        /* we see the cart total updated */
        cy.contains('$141');
    });

    it("shows the cart contents when I click on the cart display", function(){

        cy.visit('http://localhost:8010/');
        cy.contains('Ocean Blue Shirt').click();
        cy.contains('form').get('input[name=quantity]').clear().type(3);
        cy.get('form').submit();
        /* add a second product */
        cy.contains('Black Leather Bag').click();
        cy.contains('form').get('input[name=quantity]').clear().type(1);
        cy.get('form').submit();

        cy.contains("Show Cart").click();

        cy.contains("div", "Your Shopping Cart").within(($cart) => {

            /* look for product names and quantities in a table */
            cy.contains("td", "Ocean Blue Shirt").next().contains("3");
            cy.contains("td", "Black Leather Bag").next().contains("1");
            /* look for the overall cost */
            cy.contains("141")
        })



    })


})