<!DOCTYPE html>
<html lang="tj">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Marzbon UC Store</title>
  <style>
    body { font-family: Arial, sans-serif; background: #121212; color: white; margin: 0; padding: 0; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    h1 { text-align: center; color: #ffd700; }
    button { background: #28a745; color: white; border: none; padding: 12px; margin: 8px 0; width: 100%; border-radius: 8px; font-size: 16px; }
    .btn-small { padding: 8px; font-size: 14px; }
    .card { background: #1e1e1e; padding: 15px; margin: 10px 0; border-radius: 10px; }
    select, input { width: 100%; padding: 10px; margin: 8px 0; border-radius: 8px; border: none; }
    .hidden { display: none; }
    .lang-btn { background: #444; padding: 8px; margin: 5px; border-radius: 5px; }
    .total { font-size: 20px; color: #ffd700; text-align: center; margin: 20px 0; }
    .cart-item { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #333; }
  </style>
</head>
<body>
  <div class="container">
    <h1 id="title">Марзбон UC Store</h1>

    <!-- Интихоби забон -->
    <div id="lang-select">
      <p>🌐 Забонро интихоб кунед:</p>
      <button class="lang-btn" onclick="setLang('tj')">🇹🇯 Тоҷикӣ</button>
      <button class="lang-btn" onclick="setLang('ru')">🇷🇺 Русский</button>
      <button class="lang-btn" onclick="setLang('en')">🇬🇧 English</button>
      <button class="lang-btn" onclick="setLang('fa')">🇮🇷 فارسی</button>
    </div>

    <!-- Телефон -->
    <div id="phone-screen" class="hidden">
      <p id="phone-text">🔐 Рақами телефони худро ворид кунед:</p>
      <input type="tel" id="phone-input" placeholder="+992..." />
      <button onclick="login()">📱 Ворид шудан</button>
    </div>

    <!-- Менюи асосӣ -->
    <div id="main-menu" class="hidden">
      <button onclick="showScreen('catalog')">🛍 Маҳсулот</button>
      <button onclick="showScreen('wishlist')">❤️ Дилхоҳҳо</button>
      <button onclick="showScreen('cart')">🛒 Сабад</button>
      <button onclick="showScreen('freeuc')">🎁 UC ройгон</button>
      <button onclick="showInfo()">ℹ Маълумот</button>
      <button onclick="showScreen('lang-select')">🌐 Забон</button>
    </div>

    <!-- Каталог -->
    <div id="catalog" class="hidden">
      <h2 id="catalog-title">🪙 UC</h2>
      <div id="items"></div>
      <button onclick="showScreen('main-menu')">⬅️ Бозгашт</button>
    </div>

    <!-- Сабад -->
    <div id="cart" class="hidden">
      <h2>🛒 Сабад</h2>
      <div id="cart-items"></div>
      <div class="total" id="total">Ҷамъ: 0 TJS</div>
      <button onclick="checkout()" id="checkout-btn" class="hidden">📦 Фармоиш</button>
      <button onclick="clearCart()">🗑️ Пок кардан</button>
      <button onclick="showScreen('main-menu')">⬅️ Бозгашт</button>
    </div>

    <!-- Фармоиш -->
    <div id="checkout-screen" class="hidden">
      <h2>📦 Фармоиш</h2>
      <p>🎮 ID-и бозиро ворид кунед (8–15 рақам):</p>
      <input type="text" id="gameid" placeholder="123456789" />
      <p>Тарзи пардохт:</p>
      <button onclick="pay('visa')">💳 VISA</button>
      <button onclick="pay('sber')">🏦 SberBank</button>
      <button onclick="showScreen('cart')">⬅️ Бозгашт</button>
    </div>

    <!-- UC ройгон -->
    <div id="freeuc" class="hidden">
      <h2>🎁 UC ройгон</h2>
      <p id="free-balance">Тавозун: 10 UC</p>
      <button onclick="dailyUC()">🎲 UC рӯзона</button>
      <button onclick="claimUC(60)">🎁 60 UC гирифтан</button>
      <button onclick="claimUC(325)">🎁 325 UC гирифтан</button>
      <button onclick="showScreen('main-menu')">⬅️ Бозгашт</button>
    </div>
  </div>

  <script>
    const TOKEN = "8524676045:AAE7Eb_BDZKaB98-SHis2t4Pdrjgi-UodzY"; // Токени боти шумо
    const CHAT_ID = "8436218638"; // ID-и админ (шумо)

    let lang = "tj";
    let phone = "";
    let cart = {};
    let wishlist = [];
    let freeUC = 10;

    const texts = {
      tj: {
        title: "Марзбон UC Store",
        phone_text: "🔐 Рақами телефони худро ворид кунед:",
        login: "📱 Ворид шудан",
        products: "🛍 Маҳсулот",
        wishlist: "❤️ Дилхоҳҳо",
        cart: "🛒 Сабад",
        free_uc: "🎁 UC ройгон",
        info: "ℹ Маълумот",
        catalog_title: "🪙 UC",
        add_cart: "🛒 Ба сабад",
        add_wish: "❤️ Ба дилхоҳҳо",
        total: "Ҷамъ",
        checkout: "📦 Фармоиш",
        clear: "🗑️ Пок кардан",
        gameid: "🎮 ID-и бозиро ворид кунед (8–15 рақам):",
        receipt: "✅ Пас аз пардохт квитанцияро ҳамчун акс фиристед.",
        thank_you: "✅ Фармоиш қабул шуд! Админ тасдиқ мекунад.",
        daily: "🎁 Имрӯз +{n} UC!",
        not_enough: "❌ UC кофӣ нест.",
      },
      ru: {
        title: "Marzbon UC Store",
        phone_text: "🔐 Введите номер телефона:",
        login: "📱 Войти",
        products: "🛍 Товары",
        wishlist: "❤️ Избранное",
        cart: "🛒 Корзина",
        free_uc: "🎁 Бесплатные UC",
        info: "ℹ Информация",
        catalog_title: "🪙 UC",
        add_cart: "🛒 В корзину",
        add_wish: "❤️ В избранное",
        total: "Итого",
        checkout: "📦 Оформить",
        clear: "🗑️ Очистить",
        gameid: "🎮 Введите игровой ID (8–15 цифр):",
        receipt: "✅ После оплаты отправьте чек фото.",
        thank_you: "✅ Заказ принят! Админ подтвердит.",
        daily: "🎁 Сегодня +{n} UC!",
        not_enough: "❌ Недостаточно UC.",
      },
      // en ва fa ҳам илова карда мешавам, агар лозим бошад
    };

    const items = {
      1: {name: "60 UC", price: 10},
      2: {name: "325 UC", price: 50},
      3: {name: "660 UC", price: 100},
      4: {name: "1800 UC", price: 250},
      5: {name: "3850 UC", price: 500},
      6: {name: "8100 UC", price: 1000},
      101: {name: "Elite Pass", price: 110},
      102: {name: "Elite Pass Plus", price: 260},
    };

    function tr(key) {
      return texts[lang][key] || key;
    }

    function setLang(l) {
      lang = l;
      document.getElementById("title").innerText = tr("title");
      updateTexts();
      showScreen('phone-screen');
    }

    function updateTexts() {
      document.querySelectorAll("[id]").forEach(el => {
        const id = el.id;
        if (tr(id)) el.innerText = tr(id);
      });
    }

    function login() {
      phone = document.getElementById("phone-input").value;
      if (phone.length < 9) return alert("Рақам нодуруст!");
      freeUC = 10;
      showScreen('main-menu');
      loadCatalog();
    }

    function showScreen(id) {
      document.querySelectorAll(".container > div").forEach(d => d.classList.add("hidden"));
      document.getElementById(id).classList.remove("hidden");
      if (id === 'cart') updateCart();
    }

    function loadCatalog() {
      const div = document.getElementById("items");
      div.innerHTML = "";
      for (let id in items) {
        const item = items[id];
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
          <strong>${item.name}</strong> — ${item.price} TJS
          <div>
            <button class="btn-small" onclick="addToCart(\( {id})"> \){tr("add_cart")}</button>
            <button class="btn-small" onclick="addToWishlist(\( {id})"> \){tr("add_wish")}</button>
          </div>
        `;
        div.appendChild(card);
      }
    }

    function addToCart(id) {
      cart[id] = (cart[id] || 0) + 1;
      alert(tr("add_cart") + ": " + items[id].name);
      updateCart();
    }

    function updateCart() {
      const div = document.getElementById("cart-items");
      div.innerHTML = "";
      let total = 0;
      for (let id in cart) {
        const qty = cart[id];
        const item = items[id];
        total += item.price * qty;
        const el = document.createElement("div");
        el.className = "cart-item";
        el.innerHTML = `\( {item.name} x \){qty} = ${item.price * qty} TJS`;
        div.appendChild(el);
      }
      document.getElementById("total").innerText = tr("total") + `: ${total} TJS`;
      document.getElementById("checkout-btn").classList.toggle("hidden", total === 0);
    }

    function clearCart() {
      cart = {};
      updateCart();
    }

    function checkout() {
      if (Object.keys(cart).length === 0) return;
      showScreen('checkout-screen');
    }

    function pay(method) {
      const gameid = document.getElementById("gameid").value;
      if (!/^\d{8,15}$/.test(gameid)) return alert("ID хатост!");

      let msg = `📦 Фармоиши нав!\n👤 Тел: ${phone}\n🎮 ID: ${gameid}\n💳 ${method.toUpperCase()}\n\n`;
      let total = 0;
      for (let id in cart) {
        const item = items[id];
        msg += `\( {item.name} x \){cart[id]} = ${item.price * cart[id]} TJS\n`;
        total += item.price * cart[id];
      }
      msg += `\n💰 Ҷамъ: \( {total} TJS\n\n \){tr("receipt")}`;

      sendToTelegram(msg);
      alert(tr("thank_you"));
      cart = {};
      showScreen('main-menu');
    }

    function dailyUC() {
      const n = Math.floor(Math.random() * 5) + 1;
      freeUC += n;
      alert(tr("daily").replace("{n}", n));
      document.getElementById("free-balance").innerText = `Тавозун: ${freeUC} UC`;
    }

    function claimUC(amount) {
      if (freeUC < amount) return alert(tr("not_enough"));
      const gameid = prompt("🎮 PUBG ID-ро ворид кунед:");
      if (!/^\d{8,15}$/.test(gameid)) return alert("ID хатост!");
      freeUC -= amount;
      sendToTelegram(`🎁 FREE UC дархост!\n👤 Тел: ${phone}\n🎮 ID: ${gameid}\nПакет: ${amount} UC`);
      alert("✅ Дархост фиристода шуд!");
      document.getElementById("free-balance").innerText = `Тавозун: ${freeUC} UC`;
    }

    function sendToTelegram(text) {
      const url = `https://api.telegram.org/bot\( {TOKEN}/sendMessage?chat_id= \){CHAT_ID}&text=${encodeURIComponent(text)}`;
      fetch(url);
    }

    function showInfo() {
      alert("Админ: @MARZBON_TJ\nInstagram: marzbontj");
    }

    // Оғози аввал
    setLang('tj');
  </script>
</body>
</html>