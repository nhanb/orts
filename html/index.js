const fadeUpdate = (element, newValue) => {
  element.classList.add('fade');
  element.innerHTML = newValue;
  // Assuming whole animation duration == 1s
  setTimeout(() => {element.classList.remove('fade');}, 1000);
};

const drawState = (state) => {
  // Ideally I'd want to keep a global `state` object to compare against the new one and
  // only query & update DOM elements on changed fields. But hey I haven't seen dropped
  // frames even with the current query-all-the-things setup :)

  Object.keys(state).forEach(key => {
    // Assuming each state key matches an HTML element ID.
    const element = document.querySelector(`#${key}`);
    const newValue = state[key];

    if (newValue !== element.innerHTML) {
      fadeUpdate(element, newValue);
    }

  });
};

const pollState = () => {
  fetch('state.json')
    .then((response) => response.json())
    .then(drawState);
};

// Immediately populate data to avoid empty values on page load
pollState();

setInterval(pollState, 1500);
