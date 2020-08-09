var id = []
var testData = []
function testIssue() {
    var x = document.getElementById("testIssue");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
$('.select2').select2({
    theme: 'bootstrap4'
});

if($('#testName').val() != null){
    $('#addTest').prop('disabled', false);
} else {
    $('#addTest').prop('disabled', true);
}

$('#addTest').click(function(e){
    e.preventDefault()
    $.ajax({
        url: "/testDetails",
        type: "post",
        data: {
            "testId": $('#testName').val()
        },
        dataType: "json",
        success: function(res) {
            var table = ''
            var amount = 0
            var totalamount = 0
            id.push(res.id)
            testData.push(res)
            $('#formData').show()
            for(i=0; i<testData.length; i++) {
                amount = testData[i].rate
                totalamount += amount
                table += `<tr>
                    <td scope="row">`+testData[i].name+`</td>
                    <td>`+testData[i].rate+`</td>
                </tr>`
            }
            $('#returnData').html(table)
            $('#totalAmount').html(totalamount)
            $('#submitId').val(id)
        }
    });
});