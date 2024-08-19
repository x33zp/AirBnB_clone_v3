$( document ).ready(function () {
    let lsAmenity = []

   $('input[type=checkbox]').change(function () {
    const amenityName = $(this).attr('data-name');
    if ($(this).is(':checked')) {
        lsAmenity.push(amenityName);
    } else {
        lsAmenity = lsAmenity.filter(amenity => amenity !== amenityName);
    }
    $('.amenities h4').text(lsAmenity.join(', '));
   });
});
