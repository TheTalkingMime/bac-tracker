const futureDate = new Date('2024-05-24T12:00:00').getTime();

setInterval(() => {
    const now = new Date().getTime();
    const distance = futureDate - now;

    const hours = Math.floor(distance / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    const timerDisplay = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    document.getElementById('timer').textContent = timerDisplay;
}, 1000);


var eventSource = new EventSource("/events");
var img = document.createElement('img');

// Set the src attribute of the image to the path of your custom image
img.src = 'static/warning.png'; 


img.alt = 'Warning'; 

img.style.width = '.8em'; 
img.style.height = '.8em'; 
img.style.verticalAlign = 'middle';
img.style.marginRight = '15px';
img.style.marginLeft = '15px';
// Append the image to the warning element
var warningElement = document.getElementById('warning');

eventSource.onmessage = function(event) {
    console.log(event)
    var eventData = event.data.split('\n')
    document.getElementById('adv-count').innerHTML = eventData[0];
    console.log(eventData[1])
    if (eventData[1] == 'None') {
        return
    } 

    if (eventData[1] != '') {
        warningElement = document.getElementById('warning');
        warningElement.innerHTML = '';
        warningElement.appendChild(img);
        warningElement.appendChild(document.createTextNode(eventData[1]))
    } else {
        document.getElementById('warning').innerHTML = '';
    }
};