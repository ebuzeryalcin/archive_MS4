/*
    Logic/payment flow from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

//  Stripe Public key and client secret using jquery
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
// To setup up stripe and connect to base.html script
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
// Card element styles
var style = {
    base: {
        color: 'white',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        iconColor: 'white',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

// Handle for realtime validation errors on card element

// Listener for card event checking errors if there is a change
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    // Giving error message when card number is invalid at checkout.html
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
var form = document.getElementById('payment-form');
// Preventing default post action
form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    // Triggering loading overlay
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        // If there is an error message showes up
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            // If error reversing submit
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);
            // Allowing user to fix card error
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                // Showing success
                form.submit();
            }
        }
    });
});