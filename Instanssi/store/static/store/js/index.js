!function(t){function e(a){if(n[a])return n[a].exports;var s=n[a]={i:a,l:!1,exports:{}};return t[a].call(s.exports,s,s.exports,e),s.l=!0,s.exports}var n={};return e.m=t,e.c=n,e.i=function(t){return t},e.d=function(t,e,n){Object.defineProperty(t,e,{configurable:!1,enumerable:!0,get:n})},e.n=function(t){var n=t&&t.__esModule?function(){return t.default}:function(){return t};return e.d(n,"a",n),n},e.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},e.p="",e(e.s=2)}([function(t,e){"use strict";function n(t){return t.toLocaleString("fi",{style:"currency",currency:"EUR"})}function a(t){return t.toFixed(2)+" €"}function s(t,e,n){return new Promise(function(a,s){var o=new XMLHttpRequest;o.onload=function(){o.status>=200&&o.status<300?a(JSON.parse(o.responseText)):o.onerror()},o.onerror=function(){s(o.responseText?JSON.parse(o.responseText):null)},o.open(t,e),o.setRequestHeader("Accept","application/json"),o.setRequestHeader("Content-Type","application/json;charset=UTF-8"),o.send(n?JSON.stringify(n):null)})}Object.defineProperty(e,"__esModule",{value:!0});var o="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},i=!("object"!=("undefined"==typeof Intl?"undefined":o(Intl))||!Intl||"function"!=typeof Intl.NumberFormat),r=void 0;i?e.formatPrice=r=n:e.formatPrice=r=a,e.formatPrice=r,e.storeXHR=s},function(t,e){t.exports=Vue},function(t,e,n){"use strict";function a(t){return t&&t.__esModule?t:{default:t}}function s(t,e,n){return t.product.id===e.id&&(!n||t.variant&&n.id===t.variant.id)}var o=n(1),i=a(o),r=n(0);i.default.filter("formatPrice",r.formatPrice),i.default.component("store-messages",{props:{field:String,messages:Object},computed:{localMessages:function(){var t=this.messages,e=this.field;return t&&t[e]&&t[e].length>0?t[e]:null}},template:'<div><p v-if="localMessages">\n        <div class="alert alert-danger" role="alert" v-for="message in localMessages">\n            <span class="fa fa-times"></span> {{ message }}\n        </div>\n    </p></div>'}),i.default.component("store-form-group",{props:{title:String,field:String,messages:Object,update:Function,data:Object},methods:{onInput:function(t){this.$emit("update",this.field,t)}},computed:{clazz:function(){var t=this.messages,e=this.field;return t&&t[e]&&t[e].length>0?"form-group has-error":"form-group"}},template:'<div v-bind:class="clazz">\n        <label class="col-sm-4 control-label">{{ title }}</label>\n        <div class="col-sm-8">\n            <input class="form-control" @input="onInput" v-bind:value="data[field]" />\n            <store-messages :field="field" :messages="messages" />\n        </div>\n    </div>'}),i.default.component("store-information-form",{props:{messages:Object,data:Object},created:function(){this.userInfo={}},methods:{update:function(t,e){this.data[t]=e.target.value}},template:'\n<form class="form-horizontal" @submit.prevent>\n    <p>Huomaathan, että lippukoodit lähetetään annettuun sähköpostiosoitteeseen.</p>\n    <div class="row"><div class="col-lg-6">\n        <store-form-group title="Etunimi" field="first_name" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Sukunimi" field="last_name" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Sähköposti" field="email" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Vahvista sähköposti" field="email2" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Matkapuhelin" field="mobile" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Muu puhelinnumero" field="telephone" @update="update" :messages="messages" :data="data" />\n    </div>\n    <div class="col-lg-6">\n        <store-form-group title="Katuosoite" field="street" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Postinumero" field="postal_code" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Kaupunki" field="city" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Maa" field="country" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Yritys" field="company" @update="update" :messages="messages" :data="data" />\n    </div></div>\n    <div class="form-group">\n        <label class="col-lg-2 control-label">Lisätietoja</label>\n        <div class="col-lg-10">\n            <textarea class="form-control" @input="update(\'information\', $event)" v-bind:value="data.information"></textarea>\n            <store-messages field="information" :messages="messages" />\n        </div>\n    </div>\n    <div class="form-group">\n        <div class="col-sm-12">\n            <label class="control-label">\n                <input type="checkbox" v-model="data.read_terms" />\n                <span>\n                    Olen lukenut <a target="_blank" href="/store/terms">toimitusehdot</a> ja hyväksyn ne.\n                </span>\n            </label>\n            <store-messages field="read_terms" :messages="messages" />\n        </div>\n    </div>\n    <div class="clearfix"></div>\n</form>\n'}),i.default.component("store-product",{props:{product:Object,cart:Array,messages:Object},data:function(){return{variant:null}},methods:{addItem:function(){this.$emit("addItem",this.product,this.variant)}},created:function(){var t=this.product;t.variants&&t.variants.length&&(this.variant=t.variants[0])},computed:{cartCount:function(){var t=this.product,e=this.variant;if(!this.cart)return 0;var n=this.cart.findIndex(function(n){return s(n,t,e)});return n<0?0:this.cart[n].count}},template:'\n    <div class="product">\n        <span class="pull-right">\n            <span class="product-cart-count" v-if="cartCount > 0">\n                <span class="fa fa-shopping-cart"></span> {{ cartCount }}\n            </span>\n            <select class="product-variants" v-if="product.variants && product.variants.length > 0" v-model="variant">\n                <option v-for="variant in product.variants" v-bind:value="variant">\n                    {{ variant.name }}\n                </option>\n            </select>\n            <button class="btn btn-success" v-on:click="addItem()">\n                <span class="fa fa-plus" /> Lisää\n            </button>\n        </span>\n        <div>\n            <img :src="product.imagefile_thumbnail_url" width="48" height="48" />\n            {{ product.name }} ({{ product.price | formatPrice }})\n            <p class="small" v-if="product.description" v-html="product.description"></p>\n            <p v-if="product.discount_amount > 0">\n                <span class="fa fa-info"/>\n                {{ product.discount_percentage }} % alennus, jos ostat ainakin {{ product.discount_amount }} kappaletta!\n            </p>\n        </div>\n        <span class="clearfix"></span>\n    </div>\n    '});new i.default({el:"#store",data:{products:[],cart:[],messages:{},info:{first_name:"",last_name:"",email:"",street:"",postal_code:"",city:"",country:"",mobile:"",telephone:"",company:"",information:"",read_terms:!1},totalPrice:0},template:'\n<div>\n<h3>Tuotteet</h3>\n<div class="list-unstyled store-items">\n    <store-product v-for="product in products"\n        :product="product" :cart="cart" :messages="messages"\n        v-on:addItem="addItem" />\n</div>\n<h3>Ostoskori</h3>\n<store-messages field="items" :messages="messages" />\n<div class="list-unstyled store-items">\n    <div v-for="item in cart">\n        <div class="pull-left">\n            <span>{{ item.product.name }}</span>\n            <span v-if="item.variant">({{ item.variant.name }})</span>\n        </div>\n        <span class="pull-right">\n            x {{ item.count }} = {{ getSubtotal(item) | formatPrice }}\n            <button class="btn btn-secondary" v-on:click="changeItemCount(item, 1)">+</button>\n            <button class="btn btn-secondary" v-on:click="changeItemCount(item, -1)">-</button>\n            <button class="btn btn-danger" v-on:click="removeItem(item)">\n                <span class="fa fa-fw fa-trash"></span>\n            </button>\n        </span>\n        <span class="clearfix"></span>\n    </div>\n    <div>Yhteensä: {{ totalPrice | formatPrice }}</div>\n</div>\n<h3>Tiedot</h3>\n<store-information-form v-on:infoUpdate="updateInfo" :data="info" :messages="messages" />\n<span class="pull-right">\n    <button class="btn btn-primary" @click="submit">Jatka &gt;</button>\n</span>\n</div>\n  ',created:function(){var t=this;(0,r.storeXHR)("GET","/api/store_items/?format=json").then(function(e){e.forEach(function(t){t.price=parseFloat(t.price)}),t.products=e}).catch(function(t){console.error("error fetching store items:",t)})},methods:{getSubtotal:function(t){var e=1,n=t.product.discount_amount,a=(100-t.product.discount_percentage)/100;return n&&t.count>=n&&(e*=a),t.product.price*t.count*e},updateCart:function(){var t=0,e=this;this.cart.forEach(function(n){t+=e.getSubtotal(n)}),this.totalPrice=t},addItem:function(t,e){var n=this.cart.findIndex(function(n){return s(n,t,e)});if(n>=0){var a=Object.assign({},this.cart[n]);a.count++,this.cart.splice(n,1,a)}else this.cart.push({count:1,product:t,variant:e});this.updateCart()},updateInfo:function(t){this.userInfo=t},removeItem:function(t){var e=this.cart.indexOf(t);this.cart.splice(e,1),this.updateCart()},changeItemCount:function(t,e){var n=this.cart.indexOf(t),t=this.cart[n];return t.count+e<=0?this.removeItem(t):(t.count+=e,this.cart.splice(n,1,t),void this.updateCart())},getTransactionObject:function(){var t=Object.assign({},info);t.items=this.cart.map(function(t){return{item_id:t.product.id,variant_id:t.variant?t.variant.id:null,amount:t.count}})},submit:function(){var t=this,e=this.info,n=e.email,a=e.email2;if(n!==a)return void(this.messages={email:["Kirjoita sama sähköpostiosoite kahdesti."],email2:["Kirjoita sama sähköpostiosoite kahdesti."]});var s=this.getTransactionObject();(0,r.storeXHR)("POST","/api/store_transaction/?format=json",s).then(function(t){console.info(t)},function(e){t.messages=e,e&&(e.email2=e.email)}).catch(function(t){console.error(t)})}}})}]);