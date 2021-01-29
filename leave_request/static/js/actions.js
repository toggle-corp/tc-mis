(function ($) {
  $(document).ready(function () {
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
          var cookie = $.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }

    $(".leave_request_btn").click(function (e) {
      _status = $(this).attr("id");
      _id = $(this).attr("value");

      if (_status == "reject") {
        var r = confirm("Are you sure you want to reject it!");
        if (r == true) {
          window.open(`reject/${_id}/`);
        }
      } else {
        url = `actions/`;
        $.ajax({
          url: url,
          type: "POST",
          data: {
            csrfmiddlewaretoken: getCookie("csrftoken"),
            id: _id,
            status: _status,
          },
          success: function (data) {
            if (data.msg == "SUCCESS") location.reload();
          },
          error: function (error) {
            console.log(error);
          },
        });
      }
    });
  });
})(django.jQuery);
