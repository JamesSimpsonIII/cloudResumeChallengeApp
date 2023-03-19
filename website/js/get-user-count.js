// First, we need to get a reference to the button element
const button = document.getElementById('button');
const output = document.getElementById('button-output') 

// Next, we'll define a function that makes the API call
const makeApiCall = () => {
  // Replace 'API_ENDPOINT' with the URL of your API
  fetch('https://efv7k3rrepz3g7fcbk66lgqmpm0hwxrw.lambda-url.us-east-1.on.aws/')
    .then(response => response.json())
    .then(data => {
      // Do something with the data here
      output.innerHTML = data
      console.log(data);
    })
    .catch(error => {
      // Handle any errors here
      console.error(error);
    });
}

// Finally, we'll add an event listener to the button that calls the function when the button is clicked
button.addEventListener('click', makeApiCall);
