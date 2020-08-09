var id = []
var qty = []
var medData = []

function medicineIssue() {
    var x = document.getElementById("medicineIssue");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

$('.select2').select2({
    theme: 'bootstrap4'
});

$('#medicineName').change(function(){
    $('#addMedicine').prop('disabled', true);
    if($('#medicineName').val() != 0) {
        qtylist = ''
        $.ajax({
            url: "/medicineQuantity",
            type: "post",
            data: {
                "id": $('#medicineName').val()
            },
            dataType: "json",
            success: function(res) {
                for (i=0; i<=parseInt(res); i++) {
                    qtylist += `<option value="`+i+`">`+i+`</option>`
                }
                $('#quantity').html(qtylist)
            }
        });
    } else {
        $('#quantity').html(`<option value="0">Select Medicine Name First</option>`)
    }
});

$('#quantity').change(function(){
    if($('#quantity').val() == '0'){
        $('#addMedicine').prop('disabled', true);
    } else {
        $('#addMedicine').prop('disabled', false);
    }
});

$('#addMedicine').click(function(e){
    e.preventDefault()
    console.log($('#medicineName').val())
    var quantity = $('#quantity').val()
    $.ajax({
        url: "/medicineDetails",
        type: "post",
        data: {
            "id": $('#medicineName').val()
        },
        dataType: "json",
        success: function(res) {
            var table = ''
            var amount = 0
            var totalamount = 0
            res.quantity = parseInt(quantity)
            id.push(res.id)
            qty.push(res.quantity)
            medData.push(res)
            $('#formData').show()
            for(i=0; i<medData.length; i++) {
                amount = medData[i].rate*medData[i].quantity
                totalamount += amount
                table += `<tr>
                    <td scope="row">`+medData[i].name+`</td>
                    <td>`+medData[i].quantity+`</td>
                    <td>`+medData[i].rate+`</td>
                    <td>`+amount+`</td>
                </tr>`
            }
            $('#returnData').html(table)
            $('#totalAmount').html(totalamount)
            $('#submitId').val(id)
            $('#submitQty').val(qty)
        }
    });
});