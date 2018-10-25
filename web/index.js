const fadeUpdate = (element, newValue, updateFunc) => {
  element.classList.add('fade');
  updateFunc();
  // Assuming whole animation duration == 1s
  setTimeout(() => {element.classList.remove('fade');}, 1000);
};


const getDiff = (newState, oldState) => {
  const diff = {};
  Object.keys(newState).forEach(key => {
    if (newState[key] !== oldState[key]) {
      diff[key] = {
        'old': oldState[key],
        'new': newState[key],
      };
    }
  });
  return diff;
};


const drawDiffToDom = (diff) => {
  Object.keys(diff).forEach(key => {
    const element = document.querySelector(`#${key}`);
    if (!element) {return}; // skip fields not used in DOM

    const newValue = diff[key]['new'];
    const oldValue = diff[key]['old'];

    // Most elements are straightforward to overwrite
    let updateFunc = () => { element.innerHTML = newValue; };

    // Country flags are a bit more involved because of flag-icon-css lib usage
    if (key === 'p1country' || key === 'p2country') {
      updateFunc = () => {
        element.classList.remove(`flag-icon-${oldValue}`);
        element.classList.add(`flag-icon-${newValue}`);
      };
    }

    fadeUpdate(element, newValue, updateFunc);

  });
};


const applyNewState = (newState) => {
  // first calculate just what has changed
  const diff = getDiff(newState, window.STATE);

  // then only draw the changed stuff to DOM, complete with animation
  drawDiffToDom(diff);

  // advance the global state
  window.STATE = newState;
};


const pollState = () => {
  fetch('state.json')
    .then((response) => response.json())
    .then(applyNewState);
};


/*
 * ACTUAL CODE FLOW STARTS HERE
 */
window.STATE = {}; // state singleton, globally accessible
pollState(); // immediately populate data to avoid empty values on page load
setInterval(pollState, 1500);
