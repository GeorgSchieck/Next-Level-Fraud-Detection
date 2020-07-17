<template>
  <div id="hero">
    <div class="hero-container">
      <div class="wow fadeIn">
        <h1>Welcome to the Fraud Detector</h1>
        <h2>Please enter Transaction Data</h2>
        <FormulateForm @submit="submitHandler" v-model="formValues" name="form">
          <div class="input_wrap">
            <div class="inner_div">
              <FormulateInput name="nameOrig" placeholder="Origin"></FormulateInput>
              <FormulateInput name="nameDest" placeholder="Destination"></FormulateInput>
              <FormulateInput name="amount" placeholder="Amount"></FormulateInput>
              <FormulateInput type="select" name="type" placeholder="Type"
                              :options="{PAYMENT: 'Payment', TRANSFER: 'Transfer', CASH_IN: 'Cash-In', DEBIT: 'Debit', CASH_OUT: 'Cash-Out'}"></FormulateInput>
              <div class="actions">
                <FormulateInput type="submit" label="Submit"/>
              </div>
              <div v-if="isLoading">
                <div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div>
                <div><h2>Loading... ({{refCount}})</h2></div>
              </div>
              <div v-if="result['result'] == 'False'" class="nofraud"><p class="mytxt">Classified as no Fraud.</p></div>
              <div v-if="result['result'] == 'True'" class="fraud"><p class="mytxt">Transaction Classified as Fraud!</p>
              </div>

            </div>


          </div>

        </FormulateForm>
      </div>
    </div>
  </div>
</template>
<script>

  import axios from 'axios';

  export default {
    methods: {
      setLoading(isLoading) {
        if (isLoading) {
          this.refCount++;
          this.isLoading = true;
        } else if (this.refCount > 0) {
          this.refCount--;
          this.isLoading = (this.refCount > 0);
        }
     },
      submitHandler(data) {
        this.result = {}
        console.log(data.amount, data.type, data.nameOrig, data.nameDest)
        axios.post('http://h2655330.stratoserver.net:1213/post/tx', {
          amount: parseFloat(data.amount),
          type: data.type.toString(),
          nameOrig: data.nameOrig.toString(),
          nameDest: data.nameDest.toString(),

        })
          .then((response) => {
            console.log(response);
            this.$set(this.result, "result", response.data)
          }, (error) => {
            console.log(error);
          });
      }
    },
    data() {
      return {
        formValues: {},
        result: {},
        refCount: 0,
        isLoading: false
      }
    },
    created() {
      axios.interceptors.request.use((config) => {
        this.setLoading(true);
        return config;
      }, (error) => {
        this.setLoading(false);
        return Promise.reject(error);
      });

      axios.interceptors.response.use((response) => {
        this.setLoading(false);
        return response;
      }, (error) => {
        this.setLoading(false);
        return Promise.reject(error);
      });
    }

  }
</script>

<style scoped>
  .fraud {
    background: red;
    display: block;
  }

  .nofraud {
    background: green;
    display: block;
  }

  .mytxt {
    color: #FFF;
    font-size: 3em;
  }

  .input_wrap {
    text-align: center;
  }

  .inner_div {
    display: inline-block;
  }
</style>
