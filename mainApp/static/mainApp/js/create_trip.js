<script>
  document.addEventListener('DOMContentLoaded', function () {
    const totalForms = document.getElementById('id_form-TOTAL_FORMS');
    const addFormBtn = document.getElementById('add-form');
    const formContainer = document.getElementById('form-container');
    const formTemplate = document.getElementById('form-template').innerHTML;

    const cityOptions = `{{ get_city_options|safe }}`;
    let formIndex = parseInt(totalForms.value);

    addFormBtn.addEventListener('click', function () {
      const html = formTemplate
        .replace(/__prefix__/g, formIndex)
        .replace(/__ORDER__/g, formIndex + 1)
        .replace(/__CITY_OPTIONS__/g, cityOptions);

      const formBlock = document.createElement('div');
      formBlock.innerHTML = html;
      formContainer.appendChild(formBlock);

      totalForms.value = formIndex + 1;
      attachCityListeners(formIndex);
      formIndex++;
    });

    function loadStations(cityId, placeSelect) {
      if (!cityId) return;
      fetch(`/api/get-stations/?city_id=${cityId}`)
          .then(response => response.json())
          .then(data => {
            placeSelect.innerHTML = '<option value="">-- оберіть зупинку --</option>';
            data.stations.forEach(station => {
              const option = document.createElement('option');
              option.value = station.id;     // value — id станции
              option.textContent = station.name;  // текст — имя станции
              placeSelect.appendChild(option);
            });
          });
    }

    function attachCityListeners(index) {
      const fromCity = document.querySelector(`.from-city-${index}`);
      const toCity = document.querySelector(`.to-city-${index}`);

      if (fromCity) {
        fromCity.addEventListener('change', function () {
          const pair = `from-city-${index}`;
          const placeSelect = document.querySelector(`.from-place-select[data-pair="${pair}"]`);
          loadStations(this.value, placeSelect);
        });
      }

      if (toCity) {
        toCity.addEventListener('change', function () {
          const pair = `to-city-${index}`;
          const placeSelect = document.querySelector(`.to-place-select[data-pair="${pair}"]`);
          loadStations(this.value, placeSelect);
        });
      }
    }






    for (let i = 0; i < formIndex; i++) {
      attachCityListeners(i);
    }
  });
</script>
