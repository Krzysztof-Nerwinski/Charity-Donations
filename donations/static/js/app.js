document.addEventListener("DOMContentLoaded", function () {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }

  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }

  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function (e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          if (parseInt(this.$step.innerText) === 2) {
            bags_quantity = parseInt($("input[name='quantity']").val()) || 0;
            if (bags_quantity > 0) {
              this.currentStep++;
              this.updateForm();
            } else {
              alert("Musisz zadeklarować co najmniej jeden worek!")
            }
          } else if ((parseInt(this.$step.innerText) === 3) && (noOrgChecked() === true)) {
            alert("Musisz zaznaczyć co najmniej jedną organizację");
          } else if (parseInt(this.$step.innerText) === 4) {
            let failed_fields = [];
            failed_fields = checkFormInputs().join(", ");
            if (failed_fields.length > 0) {
              alert(`Wypełnij wymienione pola oznczone czerownym opisem! ${failed_fields}`)
            } else {
              fillFinalData();
              this.currentStep++;
              this.updateForm();
            }
          } else {
            this.currentStep++;
            this.updateForm();
          }
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      console.log('dziala')
      return true
      // e.preventDefault();
      // this.currentStep++;
      // this.updateForm();
    }
  }

  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }


  /* My code from this point
  * above code modified slightly*/

  let btn_next_step1 = $("#nextStep1");
  let btn_next_step2 = $("#nextStep2");
  let all_organizations = $(".organization");
  let checked_organization_name = undefined;
  let bags_quantity = 0;
  let organizations_list_title = $(`div[data-step="3"]`).children("h3");
  let messages = {
    "empty_list": "Brak organizacji przyjmujących zaznaczone przedmioty!<br> " +
      "Wróć do kroku pierwszego i zmień zaznaczenie.",
    "pick_one": "Wybierz organizacje, której chcesz pomóc:",
  };

  /* Save selected categories from step 1 and hide unfitting organizations*/
  btn_next_step1.click(() => {
    let no_organizations = true;
    let selected_categories = $("input[name='categories']:checked").map(function () {
      return $(this).val();
    }).get();
    for (let organization of all_organizations) {
      let categories = $(organization).children(".categories").text();
      let organization_valid = false;
      for (let category of categories) {
        if (selected_categories.includes(category)) {
          organization_valid = true;
        }
      }
      if (organization_valid === true) {
        organization.hidden = false;
        no_organizations = false;
      } else {
        organization.hidden = true;
      }
    }
    if (no_organizations === true) {
      organizations_list_title.html(messages["empty_list"])
    } else {
      organizations_list_title.html(messages["pick_one"])
    }
  });


  //step_3 verification
  function noOrgChecked() {
    let no_org_checked = true;
    let organization_radio = $("input[name='institution']");
    for (let org of organization_radio) {
      if (org.checked) {
        no_org_checked = false;
        checked_organization_name = $(org).nextAll(".description").children(".title").text()
      }
    }
    return no_org_checked
  }


  /* Gather all data from previous steps
  * and fill confirmation data*/
  function fillFinalData() {
    if (bags_quantity === 1) {
      $("#bags").text(`${bags_quantity} worek`)
    } else {
      $("#bags").text(`${bags_quantity} worków`)
    }
    let address = $("input[name='address']").val();
    let city = $("input[name='city']").val();
    let postcode = $("input[name='zip_code']").val();
    let phone = $("input[name='phone_number']").val();
    let pickup_date = $("input[name='pick_up_date']").val();
    let pickup_time = $("input[name='pick_up_time']").val();
    let more_info = $("textarea[name='pick_up_comment']").val();
    $("#organization").text(checked_organization_name);
    $("#address").text(address);
    $("#city").text(city);
    $("#postcode").text(postcode);
    $("#phone").text(phone);

    $("#date").text(pickup_date);
    $("#time").text(pickup_time);
    $("#moreInfo").text(`Uwagi: ${more_info}`);
  }


  //Form data verification functions
  function checkFormInputs() {
    let failed_fields = [];
    let elements = document.querySelectorAll("[required]");
    for (let el of elements) {
      let field_is_valid = true;
      let field_type = el.type.toLowerCase();
      switch (field_type) {
        case "text":
          let field_name = el.name.toLowerCase();
          field_is_valid = testInputText(el, field_name);
          break;
        case "date":
          field_is_valid = testInputDate(el);
          break;
        case "time":
          field_is_valid = testInputTime(el);
          break;
      }
      if (field_is_valid === false) {
        failed_fields.push($(el).parent().text())
      }
    }
    return failed_fields
  }

  function testInputText(input, type) {
    let pattern;
    let field_is_valid;
    switch (type) {
      case "address":
        pattern = new RegExp("^[a-zA-Z0-9\/.,ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+( [a-zA-Z0-9\/.,ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+)*$", "gi");
        break;
      case "city":
        pattern = new RegExp("^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+( [a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+)*$", "gi");
        break;
      case "zip_code":
        pattern = new RegExp("^[0-9]{2}[-][0-9]{3}$", "g");
        break;
      case "phone_number":
        pattern = new RegExp("^\\+?[0-9]+([ -][0-9]+)*([/\\][0-9]+)$", "g");
        break;
    }
    if (pattern === undefined) {
      field_is_valid = false;
      console.log("Error inside testInputText function")
    } else {
      field_is_valid = pattern.test(input.value);
    }
    addErrorToLabel(input, field_is_valid);
    return field_is_valid;
  }

  function testInputNotEmpty(input) {
    let field_is_valid = (input.value !== "");
    addErrorToLabel(input, field_is_valid);
    return field_is_valid;
  }

  function testInputDate(input) {
    let pattern = new RegExp("^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$", "gi");
    let field_is_valid = (testInputNotEmpty(input) && pattern.test(input.value));
    if (field_is_valid === true) {
      let form_date = new Date(input.value);
      let today_date = Date.now();
      if (form_date < today_date) {
        field_is_valid = false;
        alert("Wybierz datę dziesiejszą bądź późniejszą!")
      }
    }
    addErrorToLabel(input, field_is_valid);
    return field_is_valid;
  }

  function testInputTime(input) {
    let pattern = new RegExp("^[0-9]{2}\:[0-9]{2}$", "gi");
    let field_is_valid = (testInputNotEmpty(input) && pattern.test(input.value));
    addErrorToLabel(input, field_is_valid);
    return field_is_valid;
  }

  function addErrorToLabel(input, is_valid) {
    if (!is_valid) {
      $(input).parent().addClass("donation-form-error")
    } else {
      $(input).parent().removeClass("donation-form-error")
    }
  }

  let menu_elements = $(".top-menu").children().children();
  menu_elements.click(function (e) {
    setActiveElement(menu_elements, e.target);
  });


  function setActiveElement(menu_elements, target_element) {
    for (let element of menu_elements) {
      if (target_element === element) {
        $(element).addClass("active")
      } else {
        $(element).removeClass("active")
      }
    }
  }

  function checkActiveElementFromPath(menu_elements) {
    let path = window.location.href;
    $(menu_elements).each(function () {
      if (this.href === path) {
        $(this).addClass("active")
      }
    })
  }

  checkActiveElementFromPath(menu_elements)

});