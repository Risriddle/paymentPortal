$(document).ready(function () {
    // Attach the submit event handler to the form
    $('#paymentForm').submit(function (event) {
      // Prevent the default form submission
      event.preventDefault();
  
      // Collect form data
      var formData = {
        name: $('#name').val(),
        email: $('#email').val(),
        amount: $('#amount').val(),
        currency: $('#currency').val()

       
      };
  
      // Send data to the server using AJAX
      $.ajax({
        type: 'POST',
        url: '/submit_contact', // Flask route for form submission
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(formData),
        success: function (response) {
          integrate(response);
          // You can handle the server response here if needed
         
        },
        error: function (error) {
          console.error('Error submitting form:', error);
        }
      });
    });
  
    function integrate(res) {
    
      var options = {
        "key": "rzp_test_N625EvZxBFZ13r",
        "amount": res["amount"],
        "currency": res["currency"],
        "name": "Acme Corp",
        "description": "Test Transaction",
        "image": "https://example.com/your_logo",
        "order_id": res['id'],
        "handler": function (response) {
          // Handle the response data
         
          var paymentData = {
            "razorpay_payment_id": response.razorpay_payment_id,
            "razorpay_order_id": response.razorpay_order_id,
            "razorpay_signature": response.razorpay_signature,
            "name": res['notes']['name'],
            "email": res['notes']['email'],
            "amount": res['amount']
           
            // Add other payment-related data as needed
          };
          console.log(paymentData)
  
          // Send payment data to the server using AJAX
          $.ajax({
            type: 'POST',
            url: '/handle_payment', // Update with your actual Flask route for handling payments
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(paymentData),
            success: function (paymentResponse) {
              console.log('Payment handled successfully:', paymentResponse);
               // Redirect to the receipt page after handling the payment
    window.location.href = '/show_receipt?'
        

            },
            error: function (paymentError) {
              console.error('Error handling payment:', paymentError);
            }
          });
        },
        "prefill": {
          "name": res['notes']['name'],
          "email": res['notes']['email'],
          "contact": "9000090000"
        },
        "notes": {
          "address": "Razorpay Corporate Office"
        },
        "theme": {
          "color": "#3399cc"
        }
      };
  
      var rzp1 = new Razorpay(options);
      rzp1.open();
    }
  });
  