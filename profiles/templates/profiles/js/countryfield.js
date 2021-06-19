// Getting the value of country field and store as a variable
let countrySelected = $('#id_default_country').val();
// If no country selected grey color 
if(!countrySelected) {
    $('#id_default_country').css('color', '#aab7c4');
};
// If country selected 
$('#id_default_country').change(function() {
    // Taking country name value
    countrySelected = $(this).val();
    // and changing color
    if(!countrySelected) {
        $(this).css('color', '#aab7c4');
    } else {
        $(this).css('color', '#000');
    }
});