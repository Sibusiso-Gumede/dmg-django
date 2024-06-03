$('input[type="submit"]').click(function(e) {
    e.preventDefault();
});

$.widget("custom.productAutocomplete", $.ui.autocomplete, {});
$("#typeToAddProduct").productAutocomplete({
    source: "/autosuggestion/",
    minLength: 3,
    appendTo: ".type-to-add-wrapper",
    /*search: function(){
        for($child in $('input[type="radio"]')){
            if($child.hasAttribute("checked")){
                var $submitter = $("#typeToAddProduct");
                var $formData = new FormData($("#form"), $submitter);    
                
                $formData.append($child.getAttribute("name"), $child.getAttribute("value"));
                $formData.append("term", $submitter.getAttribute("value"));
                
                return fetch("/autosuggestion", {
                    method: "GET",
                    body: $formData,
                });
            }
        }
    },*/
    select: function(event){
        //if(event.key === "Enter" || event.key === "KeyUp" || event.key === "KeyDown")
        event.preventDefault();
    },
});