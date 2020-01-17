$(document).ready(() => {

    let btn_next_step1 = $("#next_step_1");
    let all_organizations = $(".organization");
    let organizations_list_title = $(`div[data-step="3"]`).children("h3");
    console.log(organizations_list_title)

    /* Save selected categories from step 1 and hide unfitting organizations*/
    btn_next_step1.on("click", () => {
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
        if (no_organizations === true){
            organizations_list_title.html("Brak organizacji przyjmujących zaznaczone przedmioty!<br>" +
                "Wróć do kroku pierwszego i zmień zaznaczenie.")
        } else {
                      organizations_list_title.html("Wybierz organizacje, której chcesz pomóc:")

        }
    })

})
;