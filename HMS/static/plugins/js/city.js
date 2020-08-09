let state_select = document.getElementById('state');
let city_select = document.getElementById('city');
state_select.onchange = function () {
    state = state_select.value;
    fetch('/city/' + state).then(function (response) {
        response.json().then(function (data) {
            let optionHTML = '';
            for (let city of data.cities) {
                optionHTML += '<option value="' + city.name + '">' + city.name + '</option>';
            }
            city_select.innerHTML = optionHTML;
        });
    });
};