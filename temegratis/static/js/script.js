function testWebP(callback) {

  var webP = new Image();
  webP.onload = webP.onerror = function () {
    callback(webP.height == 2);
  };
  webP.src = "data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA";
}

testWebP(function (support) {

  if (support == true) {
    document.querySelector('body').classList.add('webp');
  } else {
    document.querySelector('body').classList.add('no-webp');
  }
});


//Header dropdown
const dropdown = document.querySelector('.top-header__dropdown')
const dropdownList = document.querySelector('.top-header__list')

dropdown.addEventListener('click', (e) => {
  dropdownList.classList.toggle('active')
})


//Profile page

//freelancer descrpition
const toggleProfileDescription = () => {
  const shortDesc = document.querySelector('#profile__description')
  const toggleDesc = document.querySelector('#profile__toggle-description')
  const longDesc = document.querySelector('#profile__description_long')

  toggleDesc.addEventListener('click', () => {
    toggleDesc.classList.toggle('active')
    if (toggleDesc.classList.contains('active')) {
      shortDesc.style.display = 'none'
      longDesc.style.display = 'block'
    } else {
      shortDesc.style.display = 'block'
      longDesc.style.display = 'none'
    }
  })
}

try {
  toggleProfileDescription()
} catch (e) {
  console.log(e);
}

//Rating on profile page
// const redProgressBar = document.querySelectorAll('.rating-profile__progress')
const greenProgressBar = document.querySelectorAll('.rating-profile__progress-opposite')
const goodRating = document.querySelectorAll('.rating-profile__procent-good')
const badRating = document.querySelectorAll('.rating-profile__procent-bad')

for (let i = 0; i < greenProgressBar.length; i++) {
  const valuePos = goodRating[i].getAttribute('data-value')
  const valueNeg = badRating[i].getAttribute('data-value')
  greenProgressBar[i].style.width = valuePos + '%'

  if (valuePos == 100) {
    greenProgressBar[i].classList.add('hundred')
  }

  if (valuePos == 0 && valueNeg == 0) {
    greenProgressBar[i].style.width = '50%'
  }
}

//Statistics on profile page
const positiveProgressBar = document.querySelectorAll('.statistics-profile__progress-opposite')
const rating = document.querySelectorAll('.statistics-profile__nr')

for (let i = 0; i < positiveProgressBar.length; i++) {
  const percentage = rating[i].getAttribute('data-value')
  positiveProgressBar[i].style.width = percentage + '%'

  if (percentage == 0) {
    positiveProgressBar[i].style.width = '0%'
  }
}

//Info tabs on profile page
const tabs = document.querySelectorAll('.profile__info-item')
const tabBlocks = document.querySelectorAll('.profile__tab-block')
const tabsCover = document.querySelector('.profile__body')
for (let i = 0; i < tabs.length; i++) {
  tabs[i].addEventListener('click', function (e) {
    e.target.classList.toggle('active')
    tabBlocks[i].classList.toggle('active')
    tabsCover.style.minHeight = 0 + 'px'
    for(let j = 0; j <= tabs.length - 1; j++) {
      if (j != i) {
        tabs[j].classList.remove('active')
        tabBlocks[j].classList.remove('active')
      }
      //Sa fac daca apsa pe tab da nu pe altu sa nu fie minheight 0
      // if (!tab[j].classList.contains('active')) {
      //   tabsCover.style.minHeight = 220 + 'px'
      // }
    }
  })
}




///////////////
try {
  const burger = document.querySelector('.header__burger')
  const menu = document.querySelector('.header__menu')
  const body = document.querySelector('body')
  const headerList = document.querySelector('.header__list')
  burger.addEventListener('click', (e) => {
    burger.classList.toggle('active');
    menu.classList.toggle('active');
    body.classList.toggle('lock');
  })

  headerList.addEventListener('click', (e) => {
    burger.classList.remove('active');
    menu.classList.remove('active');
    body.classList.remove('lock');
  })
} catch (e) {
  console.log('Burger nav not working');
}

/*let isMobile = {
  Android: function () { return navigator.userAgent.match(/Android/i); },
  BlackBerry: function () { return navigator.userAgent.match(/BlackBerry/i); },
  iOS: function () { return navigator.userAgent.match(/iPhone|iPad|iPod/i); },
  Opera: function () { return navigator.userAgent.match(/Opera Mini/i); },
  Windows: function () { return navigator.userAgent.match(/IEMobile/i); },
  any: function () { return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows()); }
};
let body = document.querySelector('body');
if (isMobile.any()) {
  body.classList.add('touch');
  let arrow = document.querySelectorAll('.arrow');
  for (i = 0; i < arrow.length; i++) {
    let thisLink = arrow[i].previousElementSibling;
    let subMenu = arrow[i].nextElementSibling;
    let thisArrow = arrow[i];

    thisLink.classList.add('parent');
    arrow[i].addEventListener('click', function () {
      subMenu.classList.toggle('open');
      thisArrow.classList.toggle('active');
    });
  }
} else {
  body.classList.add('mouse');
}
*/
/*const popupLinks = document.querySelectorAll('.popup-link')
const body = document.querySelector('body')
const lockPadding = document.querySelectorAll('.lock-padding')

let unlock = true

const timeout = 800 // from transition

if (popupLinks.length > 0) {
  for (let i = 0; i < popupLinks.length; i++) {
    const popupLink = popupLinks[i]
    popupLink.addEventListener("click", (e) => {
      const popupName = popupLink.getAttribute('href').replace('#', '')
      const curentPopup = document.getElementById(popupName)
      popupOpen(curentPopup)
      e.preventDefault()
    })
  }
}

const popupCloseIcon = document.querySelectorAll('.close-popup')
if (popupCloseIcon.length > 0) {
  for (let i = 0; i < popupCloseIcon.length; i++) {
    const el = popupCloseIcon[i]
    el.addEventListener('click', (e) => {
      popupClose(el.closest('.popup'))
      e.preventDefault()
    })
  }
}

function popupOpen(curentPopup) {
  if (curentPopup && unlock) {
    const popupActive = document.querySelector('.popup-open')
    if (popupActive) {
      popupClose(popupActive, false)
    }
    else {
      bodyLock()
    }
    curentPopup.classList.add('open')
    curentPopup.addEventListener('click', (e) => {
      if (!e.target.closest('.popup__content')) {
        popupClose(e.target.closest('.popup'))
      }
    })
  }
}

function popupClose(popupActive, doUnlock = true) {
  if (unlock) {
    popupActive.classList.remove('open')
    if (doUnlock) {
      bodyUnLock()
    }
  }
}

function bodyLock() {
  const lockPaddingValue = window.innerWidth - document.querySelector('.wrapper').offsetWidth + 'px'
  if (lockPadding.length > 0) {
    for (let i = 0; i < lockPadding.length; i++) {
      const el = lockPadding[i]// for fixed objects ex: header
      el.style.paddingRight = lockPaddingValue
    }
  }
  body.style.paddingRight = lockPaddingValue
  body.classList.add('lock')

  unlock = false
  setTimeout(function () {
    unlock = true
  }, timeout)
}

function bodyUnlock() {
  setTimeout(function () {
    if (lockPadding.length > 0) {
      for (let i = 0; i < lockPadding.length; i++) {
        const el = lockPadding[i]
        el.style.paddingRight = '0px'
      }
    }
    body.style.paddingRight = '0px'
    body.classList.remove('lock')
  }, timeout)
}

//close on esc
document.addEventListener('keydown', (e) => {
  if (e.which === 27) {
    const popupActive = document.querySelector('.popup.open')
    popupClose(popupActive)
  }
})*/