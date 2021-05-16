//Workshop Session Logic
//If user chooses second choice in session 1, all of session 2 choices are invalid
//If user chooses third choice in session 2, only second choice in session 3 is valid
//Session 3-second choice is only valid if user selected third choice in session 2


let sessionOneOnChange = function(e) {
    console.log("sessionOneOnChange triggered ", e.currentTarget.value);
    let sessionValue = e.currentTarget.value;
    if (sessionValue == 'descriptive-settings') {
        // hide the second set of radio button
        document.querySelector('.workshop-session-two').hidden = true;
    }
    else {
        document.querySelector('.workshop-session-two').hidden = false;
    }
};
let radioButtons = document.querySelectorAll('input[type=radio][name="session-one-choice"]');
radioButtons.forEach(function(btn) {
    btn.addEventListener('change', sessionOneOnChange);
});

/**
 * validateResponse
 * @description - checks workshop options to insure valid combinations
 * @returns {boolean}
 */
function validateResponse() {
    console.log("validation activated");
    let isValid = true;

    let sessionOneValue = null;
    let sessionTwoValue = null;
    let sessionThreeValue = null;

    let sessionOneSelectedRadioElement = document.querySelector('input[type=radio][name="session-one-choice"]:checked');
    if (sessionOneSelectedRadioElement != null) {
        sessionOneValue = sessionOneSelectedRadioElement.value;
    }

    let sessionTwoSelectedRadioElement = document.querySelector('input[type=radio][name="session-two-choice"]:checked');
    if (sessionTwoSelectedRadioElement != null) {
        sessionTwoValue = sessionTwoSelectedRadioElement.value;
    }

    let sessionThreeSelectedRadioElement = document.querySelector('input[type=radio][name="session-three-choice"]:checked');
    if (sessionThreeSelectedRadioElement != null) {
        sessionThreeValue = sessionThreeSelectedRadioElement.value;
    }

        console.log(sessionOneValue);
        console.log(sessionTwoValue);
        console.log(sessionThreeValue);
    let errors = [];

    //LAR: I fixed this one, but didn't address other invalid combinations
    if (sessionOneValue == null || (sessionOneValue != 'descriptive-settings' && sessionTwoValue == null) || sessionThreeValue == null) {
        errors.push("Make sure all fields are selected.  ");
        isValid =  false;
    }
    if ((sessionTwoValue == 'char-development' && sessionThreeValue != 'plot-structure')){
        errors.push("You chose 'Character Development: Creating Memorable Characters' in Session 2, you may only chose 'How to Plot and Structure a Novel' in Session 3");
    }
    if (sessionThreeValue == 'plot-structure' && (sessionOneValue == 'descriptive-settings' || sessionTwoValue != 'char-development')) {
        errors.push("You cannot sign up for 'How to Plot and Structure a Novel' in Session 3 unless you signed up for 'Character" +
            " Development: Creating Memorable Characters' in Session 2");
    }

    if (errors.length > 0) {
        let message = errors.join("\n");
        openWindow(message);
        isValid = false;
    }

    return isValid;
}
/**
 * @description - opens a new window, centered, and displays the error message
 * @param message - error message to display
 */
function openWindow(message) {
    //pop-up window centering
    let width = 500;
    let height = 400;
    let left = (screen.width/2) - (width/2);
    let top = (screen.height/2) - (height/2);

    let errorWindow = window.open('err', 'temp', "width="+width+",height="+height+",top="+top+",left="+left);
    errorWindow.document.write(message);
}
/**
 * Function to retrieve the votes cast for each radio button selection
 */
function getVotes() {
    let votes = JSON.parse(localStorage.getItem('votes'));

    if (!votes) {
        votes = {};
        document.querySelectorAll('.vote-count').forEach(input => {
            votes[input.value] = 0;
        })
    }
    return votes;
}

//On-Click alert event for the poll submission radio buttons
const pollSubmit = document.getElementById('poll-submit');
pollSubmit && pollSubmit.addEventListener('click',function(event) {
    // Prevents default form submit event
    event.preventDefault()

    // Getting the selected one
    let selected = document.querySelector('input[type=radio][name=author-nom]:checked');

    // Get votes object
    let votes = getVotes();

    // Add vote
    votes[selected.value]++;

    // Save votes into localStorage
    localStorage.setItem('votes', JSON.stringify(votes));

    // Show updated votes state
    showVotes();

    // Show a success message to the user
    alert("Thank you for voting for " + selected.value + ".");

});

/**
 * Cookie function to set the user information from the registration form
 */
const confID = document.getElementById('confID');
confID && confID.addEventListener('change', autocompleteRegistration);
function setCookie(){
    let obj = {};
    const inputs = [
        "nameTitle",
        "firstName",
        "lastName",
        "streetAddress",
        "city",
        "states",
        "zipcode",
        "phone",
        "email",
        "employer",
        "website",
        "job-pos"
    ]

    for (let input of inputs) {
        obj[input] = document.getElementById(input).value;
    }

    const id = document.getElementById('confID').value;
    let jsonString = id + '=' + JSON.stringify(obj);
    document.cookie = jsonString;
    console.log(document.cookie);
}

/**
 * Function to retrieve the stored cookie values based on the conference ID and autofill form input
 */
function autocompleteRegistration(event) {
    const id = event.target.value;

    if (!document.cookie) {
        return console.log('No cookie yet!')
    }

    const cookies = document.cookie.split('; ').reduce((cookies, cookie) => {
        const [id, inputs] = cookie.split('=');
        if (id.match(/^\d+$/)) {
            cookies[id] = JSON.parse(inputs);
        }
        return cookies;
    }, {})

    const inputs = cookies[id];

    if (!inputs) {
        return console.log('Conference', id, 'not found in', cookies);
    }

    // this for of is the same as .forEach
    const entries = Object.entries(inputs);

    for (const [id, value] of entries) {
        document.getElementById(id).value = value;
        // .checked attr for checkboxes and input radio
        // if (input is checkbox or radio) input.checked = isChecked?
    }
}
/**
 * Function to use innerHTML to display the votes for each radio button selection
 */
function showVotes() {
    Object.entries(getVotes()).forEach(([name, votes]) => {
        console.log('this is', name, 'and has', votes, 'votes')
        document.querySelector(`input[value="${name}"]`).parentNode.querySelector('.total-votes').innerHTML = votes;
    })
}
