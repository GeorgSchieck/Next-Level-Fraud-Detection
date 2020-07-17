<template>
  <div id="contact">


    <div class="container wow fadeInUp">

      <div class="row">
        <div class="col-md-12">
          <h3 class="section-title">Indice risk analysis</h3>
          <div class="section-title-divider"></div>
          <p class="section-description">Please choose your risk profile</p>

        </div>
      </div>

      <div class="blue-square-container">

        <div class="blue-square">
          <p class="section-title">{{this.risk_string}}</p>
          <input v-model="risk_slider" type="range" class="custom-range" min="1" max="4" id="customRange1">
        </div>


      </div>


      <div class="row">
        <table class="table table-striped  table-hover">
          <thead>
          <tr>
            <th>Rank</th>
            <th>Fund</th>
            <th>Risk</th>
            <th>Sentiment</th>
            <th>Change</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="fund in funds_table" :key="funds.indexfonds" class="fund">
            <td>{{fund.rank}}</td>
            <td>{{fund.indexfonds}}</td>
            <td>{{fund.risk.toFixed(2)}}</td>
            <td>{{fund.avg_sentiment.toFixed(2)}}</td>
            <td>{{fund.change}}</td>
          </tr>
          </tbody>

        </table>
      </div>

    </div>

  </div>

</template>
<script>
  import axios from 'axios';

  export default {
    methods: {

      forceup: function () {
        this.$forceUpdate()
      },
      getquartiles: function (arr) {
        // sort array ascending
        const asc = arr => arr.sort((a, b) => a - b);

        const sum = arr => arr.reduce((a, b) => a + b, 0);

        const mean = arr => sum(arr) / arr.length;

// sample standard deviation
        const std = (arr) => {
          const mu = mean(arr);
          const diffArr = arr.map(a => (a - mu) ** 2);
          return Math.sqrt(sum(diffArr) / (arr.length - 1));
        };

        const quantile = (arr, q) => {
          const sorted = asc(arr);
          const pos = ((sorted.length) - 1) * q;
          const base = Math.floor(pos);
          const rest = pos - base;
          if ((sorted[base + 1] !== undefined)) {
            return sorted[base] + rest * (sorted[base + 1] - sorted[base]);
          } else {
            return sorted[base];
          }
        };

        const q25 = arr => quantile(arr, .25);

        const q50 = arr => quantile(arr, .50);

        const q75 = arr => quantile(arr, .75);

        this.q25 = q25(arr);
        this.q50 = q50(arr);
        this.q75 = q75(arr);
      }

    },
    data: function () {
      return {
        funds: [],
        funds_old: [],
        tmp: [],
        risks: [],
        risk_slider: 1,
        q25: 0,
        q50: 0,
        q75: 0
      }

    },
    computed: {
        risk_string: function() {
          if (this.risk_slider == 1) {
            return "low"
          } else if (this.risk_slider == 2) {
            return "medium"
          } else if (this.risk_slider == 3) {
            return "high"
          } else if (this.risk_slider == 4) {
            return "ultra high"
          }
        },
        funds_table: function () {
          this.tmp = [];
          if (this.risk_slider == 1) {
            this.funds.forEach((item) => {
              if (item.risk < this.q25) {
                this.tmp.push(item)
              }
            });
          } else if (this.risk_slider == 2) {
            this.funds.forEach((item) => {
              if (item.risk < this.q50) {
                this.tmp.push(item)
              }
            });
          } else if (this.risk_slider == 3) {
            this.funds.forEach((item) => {
              if (item.risk < this.q75) {
                this.tmp.push(item)
              }
            });
          } else if (this.risk_slider == 4) {
            this.funds.forEach((item) => {
              this.tmp.push(item)
            });
          } else {
            console.log("Error")
          }
          return this.tmp
        }

    },
    created: function () {
      axios
        .get('http://h2655330.stratoserver.net:5431/get/predictions/actual')
        .then(response => (this.funds = response.data.items))
        .then(response => this.funds.sort((a, b) => (a.risk > b.risk) ? 1 : -1))
        .then(response => this.funds.forEach((item, index) => {
          item.rank = index + 1
          console.log(item)
        }))
        .then(response => (axios
          .get('http://h2655330.stratoserver.net:5431/get/predictions/last')
          .then(response => (this.funds_old = response.data.items))
          .then(response => this.funds_old.sort((a, b) => (a.risk > b.risk) ? 1 : -1))
          .then(response => this.funds_old.forEach((item, index) => {
            item.rank = index + 1
            console.log(item)
          }))))
        .then(response => (this.funds.forEach((item, index) => {
          this.funds_old.forEach((item_old, index_old) => {
            if (item.indexfonds === item_old.indexfonds) {
              item.change = item.rank - item_old.rank
            }

          })
        })))
        .then(() => (this.funds.forEach((item, index) => {
          this.risks.push(item.risk)
        })))
        .then(() => (this.getquartiles(this.risks)))
        .then(() => (console.log(this.q25)))
        .then(() => (console.log(this.q50)))
        .then(() => (console.log(this.q75)))
        .then(() => (this.forceup()));
    },
    updated: function () {



    }
  }

</script>
<style>
  #contact {
    min-height: 100vh;
  }

  .blue-square-container {
    text-align: center;
  }

  .blue-square {
    width: 200px;
    height: 100px;
    display: inline-block;
  }

  .custom-range {

    display: inline-block;
  }
</style>
