<template>
  <footer id="footer">
    <div class="container">
      <div class="row align-items-end">
        <div class="col-md-6" id="address">
          <div>
            <strong>Fraud Detection</strong> inc.<br>
            Coblitzallee 1-9<br>
            68163 Mannheim<br>
            Phone: +49 12345 12345<br>
            <br>
          </div>

        </div>
        <div class="col-md-6 .offset-md-6"  id="quicklinks">
          <router-link to="/contact" tag="a">
            contact
          </router-link>
          <router-link to="/impressum" tag="a">
            Impressum
          </router-link>
          <router-link to="/agb" tag="a">
            AGB
          </router-link>
          <router-link to="/datenschutz" tag="a">
            Datenschutz
          </router-link>

        </div>
      </div>


    </div>
  </footer>
</template>
<style scoped>
  #quicklinks, #address {
    text-align: center;
  }
  a {
    display: inline;
    margin-right: 10px;
    margin-left:10px;
  }
  @media (max-width: 933px) {
    #quicklinks {
      display:block;
    }
  }
</style>
