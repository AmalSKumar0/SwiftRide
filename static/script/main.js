const menuBtn = document.getElementById("menu-btn");
const navLinks = document.getElementById("nav-links");
const menuBtnIcon = menuBtn.querySelector("i");

menuBtn.addEventListener("click", (e) => {
  navLinks.classList.toggle("open");

  const isOpen = navLinks.classList.contains("open");
  menuBtnIcon.setAttribute("class", isOpen ? "ri-close-line" : "ri-menu-line");
});

navLinks.addEventListener("click", (e) => {
  navLinks.classList.remove("open");
  menuBtnIcon.setAttribute("class", "ri-menu-line");
});

const scrollRevealOption = {
  distance: "50px",
  origin: "bottom",
  duration: 1000,
};

ScrollReveal().reveal(".header__image img", {
  ...scrollRevealOption,
  origin: "right",
});

ScrollReveal().reveal(".header__content h1", {
  ...scrollRevealOption,
  delay: 500,
});

ScrollReveal().reveal(".header__content p", {
  ...scrollRevealOption,
  delay: 1000,
});

ScrollReveal().reveal(".header__content form", {
  ...scrollRevealOption,
  delay: 1500,
});

ScrollReveal().reveal(".header__content .bar", {
  ...scrollRevealOption,
  delay: 2000,
});

ScrollReveal().reveal(".header__image__card", {
  duration: 1000,
  interval: 500,
  delay: 2500,
});


document.addEventListener('DOMContentLoaded', function () {
  let debounceTimeout1, debounceTimeout2;
  const cache = {}; // Cache object to store previous API responses
  let validSelections = { from: false, to: false }; // To track valid selections

  // Autocomplete for the first input (From)
  document.getElementById('autocomplete').addEventListener('input', function () {
      const query = this.value.trim();
      clearTimeout(debounceTimeout1);
      if (query) {
          debounceTimeout1 = setTimeout(() => fetchSuggestions(query, 'suggestions', 'from'), 300);
      } else {
          document.getElementById('suggestions').innerHTML = '';
          document.getElementById('from-error').textContent = '';
          validSelections.from = false;
      }
  });

  // Autocomplete for the second input (To)
  document.getElementById('autocomplete2').addEventListener('input', function () {
      const query = this.value.trim();
      clearTimeout(debounceTimeout2);
      if (query) {
          debounceTimeout2 = setTimeout(() => fetchSuggestions(query, 'suggestions2', 'to'), 300);
      } else {
          document.getElementById('suggestions2').innerHTML = '';
          document.getElementById('to-error').textContent = '';
          validSelections.to = false;
      }
  });

  function fetchSuggestions(query, suggestionBoxId, field) {
      if (cache[query]) {
          displaySuggestions(cache[query], suggestionBoxId, field);
          return;
      }

      const southIndiaBbox = '72.5,8.0,80.5,15.0'; // Bounding box for South India

      fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&addressdetails=1&limit=5&viewbox=${southIndiaBbox}&bounded=1`)
          .then(response => response.json())
          .then(data => {
              cache[query] = data; // Cache the results
              displaySuggestions(data, suggestionBoxId, field);
          })
          .catch(error => console.error('Error fetching Nominatim suggestions:', error));
  }

  function displaySuggestions(data, suggestionBoxId, field) {
      const suggestionsContainer = document.getElementById(suggestionBoxId);
      suggestionsContainer.innerHTML = ''; // Clear previous suggestions

      if (data.length === 0) {
          document.getElementById(`${field}-error`).textContent = 'Invalid location';
          validSelections[field] = false;
      } else {
          document.getElementById(`${field}-error`).textContent = '';
          validSelections[field] = true;
      }

      // Populate the suggestion list
      data.forEach(function (place) {
          const suggestionItem = document.createElement('div');
          suggestionItem.classList.add('suggestion-item');
          suggestionItem.textContent = place.display_name;
          suggestionItem.onclick = function () {
              document.getElementById(`autocomplete${field === 'from' ? '' : '2'}`).value = place.display_name;
              suggestionsContainer.innerHTML = ''; // Clear suggestions after selection
              validSelections[field] = true;
          };
          suggestionsContainer.appendChild(suggestionItem);
      });
  }

  function validateForm() {
      let isValid = true;

      // Validate 'From' field
      const fromInput = document.getElementById('autocomplete').value.trim();
      if (!validSelections.from || fromInput === '') {
          document.getElementById('from-error').textContent = 'Please select a valid "From" location';
          isValid = false;
      } else {
          document.getElementById('from-error').textContent = '';
      }

      // Validate 'To' field
      const toInput = document.getElementById('autocomplete2').value.trim();
      if (!validSelections.to || toInput === '') {
          document.getElementById('to-error').textContent = 'Please select a valid "To" location';
          isValid = false;
      } else {
          document.getElementById('to-error').textContent = '';
      }

      return isValid;
  }
});