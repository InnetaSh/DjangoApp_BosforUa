
  document.addEventListener('DOMContentLoaded', function () {
    const totalForms = document.getElementById('id_form-TOTAL_FORMS');
    const addFormBtn = document.getElementById('add-form');
    const formContainer = document.getElementById('form-container');
    const formTemplate = document.getElementById('form-template').innerHTML;

    const cityOptions = `{{ get_city_options|safe }}`;
    let formIndex = parseInt(totalForms.value);
    let lastSelectedStationName = '';


    addFormBtn.addEventListener('click', function () {
      const html = formTemplate
        .replace(/__prefix__/g, formIndex)
        .replace(/__ORDER__/g, formIndex + 1)
        .replace(/__CITY_OPTIONS__/g, cityOptions);

      const formBlock = document.createElement('div');
      formBlock.innerHTML = html;


       const fromSelect = formBlock.querySelector(`#id_form-${formIndex}-from_city`);
       if (fromSelect) {
         const input = document.createElement('input');
         input.type = 'text';
         input.name = fromSelect.name;
         input.className = fromSelect.className;
         input.id = fromSelect.id;
         input.placeholder = 'Введіть місто відправлення';


       if (formIndex > 0) {
         const prevToSelect = document.getElementById(`id_form-${formIndex - 1}-to_city`);
         if (prevToSelect && prevToSelect.tagName.toLowerCase() === 'select') {
           const selectedOption = prevToSelect.options[prevToSelect.selectedIndex];
           if (selectedOption) {
             input.value = selectedOption.text;
           }
         }
       }

         input.readOnly = true;
         fromSelect.replaceWith(input);
       }

       const fromPlaceSelect = formBlock.querySelector(`#id_form-${formIndex}-from_place`);
        if (fromPlaceSelect) {
          const input = document.createElement('input');
          input.type = 'text';
          input.name = fromPlaceSelect.name;
          input.className = fromPlaceSelect.className;
          input.setAttribute('data-pair', fromPlaceSelect.getAttribute('data-pair'));
          input.id = fromPlaceSelect.id || `id_form-${formIndex}-from_place`;
          input.placeholder = 'Введіть зупинку відправлення';

        if (lastSelectedStationName) {
            input.value = lastSelectedStationName;
          }

          input.readOnly = true;
          fromPlaceSelect.replaceWith(input);
        }



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
              option.value = station.id;
              option.textContent = station.name;
              placeSelect.appendChild(option);
            });

            placeSelect.addEventListener('change', () => {
                const selectedOption = placeSelect.options[placeSelect.selectedIndex];
                if (selectedOption) {
                  lastSelectedStationName = selectedOption.textContent;
                }
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

