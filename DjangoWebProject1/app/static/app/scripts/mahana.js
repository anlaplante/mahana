$(function () {
    $('.dateinput').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true
    });
});

$(document).ready(function () {

    ddlCat = $('#product-filter select[name=categoryid]');
    ddlSubcat = $('#product-filter select[name=subcategoryid]');
    ddlPdt = $('#product-filter select[name=productname]');

    ddlCat.change(function () {
        /*$('select[name=subcategoryid]').html('<option value="">----------</option>');
        cat_id = $(this).val();
        request_url = '/get_subcategories/' + cat_id + '/';
        $.ajax({
            url: request_url,
            success: function(data){
                $.each(data, function(key, value){
                    $('select[name=subcategoryid]').append('<option value="' + this.pk + '">' + this.fields.subcategoryname + '</option>');
                });

            }
        })*/
        fillsubcat(-1)
    })
    ddlSubcat.change(function () {
        fillproduct(-1)
    })
    init = function () {
        catid = $.urlParam('categoryid');
        if (catid != null) {
            subcatid = $.urlParam('subcategoryid');
            fillsubcat(subcatid);
        }
    }
    fillsubcat = function (subcatid) {
        ddlSubcat.html('<option value="">----------</option>');
        ddlPdt.html('<option value="">----------</option>');
        cat_id = ddlCat.val();
        request_url = '/get_subcategories/' + cat_id + '/';
        $.ajax({
            url: request_url,
            success: function (data) {
                $.each(data, function (key, value) {
                    $('select[name=subcategoryid]').append('<option value="' + this.pk + '">' + this.fields.subcategoryname + '</option>');
                    if (subcatid != null && subcatid > -1) {
                        //$(ddlSubcat).val(subcatid);
                        $('select[name=subcategoryid] option[value=' + subcatid + ']').attr("selected", "selected");
                        productid = $.urlParam('productname');
                        fillproduct(productid);
                    }
                });

            }
        })
    }

    fillproduct = function (productid) {
        ddlPdt.html('<option value="">----------</option>');
        subcat_id = ddlSubcat.val();
        request_url = '/get_products/' + subcat_id + '/';
        $.ajax({
            url: request_url,
            success: function (data) {
                $.each(data, function (key, value) {
                    $('select[name=productname]').append('<option value="' + this.pk + '">' + this.fields.productname + '</option>');
                    if (productid != null && productid > -1) {
                        //$(ddlSubcat).val(subcatid);
                        $('select[name=productname] option[value=' + productid + ']').attr("selected", "selected");
                    }
                });

            }
        })
    }

    $.urlParam = function (name) {
        var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
        if (results == null) {
            return null;
        } else {
            return results[1] || -1;
        }
    }

    init();
});

