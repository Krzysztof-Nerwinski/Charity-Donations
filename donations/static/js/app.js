document.addEventListener("DOMContentLoaded", function() {
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
  document.addEventListener("click", function(e) {
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
          //check if user selected any of given organizations on step_3
          if ((parseInt(this.$step.innerText) === 3) && (noOrgChecked() === true)) {
            alert("Musisz zaznaczyć co najmniej jedną organizację");
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
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }


  /* My code from this point
  * above code modified slightly*/

  let btn_next_step1 = $("#next_step_1");
  let btn_next_step2 = $("#next_step_2");
  let btn_next_last = $("#next_last_step");
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

  //step_2 check amount of bags
  btn_next_step2.click(()=>{
    bags_quantity = parseInt($("input[name='bags']").val()) || 0;
  });









});



//step_3 verification
function noOrgChecked() {
  let no_org_checked = true;
  let organization_radio = $("input[name='organization']");
  for (let org of organization_radio) {
      if (org.checked) {
        no_org_checked = false;
        checked_organization_name = $(org).nextAll(".description").children(".title").text()
      }
  }
  return no_org_checked
}

/* Gather all data from previous steps, verify
* and fill confirmation data*/
function fill_final_data(){
  btn_next_last.on("click", () => {
    if (bags_quantity === 1) {
      $("#bags").text(`${bags_quantity} worek`)
    } else {
      $("#bags").text(`${bags_quantity} worków`)
    }
    $("#organization").text(checked_organization_name);
    $("#address").text($("input[name='address']").val());
    $("#city").text($("input[name='city']").val());
    $("#postcode").text($("input[name='postcode']").val());
    $("#phone").text($("input[name='phone']").val());

    $("#date").text($("input[name='data']").val());
    $("#time").text($("input[name='time']").val());
    $("#more_info").text(`Uwagi: ${$("textarea[name='more_info']").val()}`);
  });
}
