<template>
  <div id="contact">
    <div class="container wow fadeInUp">
      <div class="row">
        <div class="col-md-12">
          <h3 class="section-title">Contact us</h3>
          <div class="section-title-divider"></div>
          <p class="section-description">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque</p>
        </div>
      </div>

      <div class="row">
        <div class="col-md-3 col-md-push-2">
          <div class="info">
            <div>
              <i class="fa fa-map-marker"></i>
              <p> Coblitzallee 1-9<br>68163 Mannheim</p>
            </div>

            <div>
              <i class="fa fa-envelope"></i>
              <p>info@fraud-detection.com</p>
            </div>

            <div>
              <i class="fa fa-phone"></i>
              <p>+49 12345 12345</p>
            </div>

          </div>
        </div>

        <div class="col-md-5 col-md-push-2">
          <div class="form">
            <div id="sendmessage">Your message has been sent. Thank you!</div>
            <div id="errormessage"></div>
            <form action="" method="post" role="form" class="contactForm">
              <div class="form-group">
                <input type="text" name="name" class="form-control" id="name" placeholder="John Doe" data-rule="minlen:4" data-msg="Please enter your name." />
                <div class="validation"></div>
              </div>
              <div class="form-group">
                <input type="email" class="form-control" name="email" id="email" placeholder="info@example.com" data-rule="email" data-msg="Please provide a valid e-mail" />
                <div class="validation"></div>
              </div>
              <div class="form-group">
                <select class="form-control" name="subject" id="subject" placeholder="Topic" data-rule="minlen:4" data-msg="Please choose topic">
                  <option value="" disabled selected hidden>Choose topic</option>
                  <option value="example1">One interesting Topic</option>
                  <option value="example2">Another interesting Topic</option>
                </select>
                <!--<input type="text" class="form-control" name="subject" id="subject" placeholder="Betreff" data-rule="minlen:4" data-msg="Bitte geben Sie einen Betreff an." />-->
                <!--<div class="validation"></div>-->
              </div>
              <div class="form-group">
                <textarea class="form-control" name="message" rows="5" data-rule="required" data-msg="Please send us a message." placeholder="Message"></textarea>
                <div class="validation"></div>
              </div>
              <div class="text-center"><button type="submit">Send message</button></div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
    export default {
      mounted: function () {
        $('form.contactForm').submit(function(){
          var f = $(this).find('.form-group'),
            ferror = false,
            emailExp = /^[^\s()<>@,;:\/]+@\w[\w\.-]+\.[a-z]{2,}$/i;

          f.children('input').each(function(){ // run all inputs

            var i = $(this); // current input
            var rule = i.attr('data-rule');

            if( rule !== undefined ){
              var ierror=false; // error flag for current input
              var pos = rule.indexOf( ':', 0 );
              if( pos >= 0 ){
                var exp = rule.substr( pos+1, rule.length );
                rule = rule.substr(0, pos);
              }else{
                rule = rule.substr( pos+1, rule.length );
              }

              switch( rule ){
                case 'required':
                  if( i.val()==='' ){ ferror=ierror=true; }
                  break;

                case 'minlen':
                  if( i.val().length<parseInt(exp) ){ ferror=ierror=true; }
                  break;

                case 'email':
                  if( !emailExp.test(i.val()) ){ ferror=ierror=true; }
                  break;

                case 'checked':
                  if( !i.attr('checked') ){ ferror=ierror=true; }
                  break;

                case 'regexp':
                  exp = new RegExp(exp);
                  if( !exp.test(i.val()) ){ ferror=ierror=true; }
                  break;
              }
              i.next('.validation').html( ( ierror ? (i.attr('data-msg') !== undefined ? i.attr('data-msg') : 'wrong Input') : '' ) ).show('blind');
            }
          });
          f.children('textarea').each(function(){ // run all inputs

            var i = $(this); // current input
            var rule = i.attr('data-rule');

            if( rule !== undefined ){
              var ierror=false; // error flag for current input
              var pos = rule.indexOf( ':', 0 );
              if( pos >= 0 ){
                var exp = rule.substr( pos+1, rule.length );
                rule = rule.substr(0, pos);
              }else{
                rule = rule.substr( pos+1, rule.length );
              }

              switch( rule ){
                case 'required':
                  if( i.val()==='' ){ ferror=ierror=true; }
                  break;

                case 'minlen':
                  if( i.val().length<parseInt(exp) ){ ferror=ierror=true; }
                  break;
              }
              i.next('.validation').html( ( ierror ? (i.attr('data-msg') != undefined ? i.attr('data-msg') : 'wrong Input') : '' ) ).show('blind');
            }
          });
          if( ferror ) return false;
          else var str = $(this).serialize();
          $.ajax({
            type: "POST",
            url: "/contactform/contactform.php",
            data: str,
            success: function(msg){
              // alert(msg);
              if(msg == 'OK') {
                $("#sendmessage").addClass("show");
                $("#errormessage").removeClass("show");
                $('.contactForm').find("input, textarea").val("");
              }
              else {
                $("#sendmessage").removeClass("show");
                $("#errormessage").addClass("show");
                $('#errormessage').html(msg);
              }

            }
          });
          return false;
        });
      }
    }

</script>
<style>
  #contact {
    min-height: 100vh;
  }
</style>
