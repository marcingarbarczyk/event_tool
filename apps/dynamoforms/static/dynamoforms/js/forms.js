class FormParser {
    constructor(form) {
        this.form = form;
        this.listenToRadioButtons();
        this.preventMultipleSubmissions();
    }

    preventMultipleSubmissions() {
        this.form.addEventListener("submit", function(event) {
            if (event.target.checkValidity()) {
                event.target.querySelector("input[type=submit]").disabled = true;
            }
        });
    }

    listenToRadioButtons() {
        let radioButtons = this.form.querySelectorAll('input[type="radio"]');
        for (let i = 0; i < radioButtons.length; i++) {
            radioButtons[i].addEventListener('change', (event) => {
                this.handleRadioButtonChange(event);
            });
        }
    }

    handleRadioButtonChange(event) {
        let fieldChoiceId = event.target.value;
        let fieldName = event.target.name;

        let sections = this.form.querySelectorAll('div[data-field="' + fieldName + '"]');
        sections.forEach((section) => {
            let sectionFieldChoiceId = section.dataset.fieldChoice;
            let requiredFields = section.getElementsByClassName('required');

            if (sectionFieldChoiceId === fieldChoiceId) {
                // when showing section, add required to fields
                for (let i = 0; i < requiredFields.length; i++) {
                    requiredFields[i].setAttribute('required', 'required');
                }
                section.classList.add('active');
            } else {
                // when hiding section, remove required from fields
                for (let i = 0; i < requiredFields.length; i++) {
                    requiredFields[i].removeAttribute('required');
                }
                section.classList.remove('active');
            }
        });
    }
}

let forms = document.getElementsByClassName('dynamoform');
for (let f = 0; f < forms.length; f++) {
    new FormParser(forms[f]);
}


// Checkbox limiter
const divs = document.querySelectorAll('div.checkbox');

divs.forEach(function(div) {
    var label = div.querySelector('label');
    var text = label.textContent;

    // if the label's text is over 100 characters
    if (text.length > 150) {
        // save the text to data attribute and also shorten it
        label.dataset.text = text;
        label.textContent = text.slice(0, 150) + '...';

        // create a Read More button
        var button = document.createElement('button');
        button.textContent = 'rozwiń';
        label.appendChild(button);

        // setup the click event handler
        button.addEventListener('click', function(event) {
            event.stopPropagation();
            label.textContent = label.dataset.text;  // restore the original text
            this.remove();  // remove the Read More button
        });
    }
});