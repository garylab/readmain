async function searchDictionary(offcanvasTitleEl, offcanvasContentEl, word, to_lang) {
    offcanvasTitleEl.innerHTML = word;

    try {
        const response = await httpGet(DICTIONARY_URL, {text: word, to_lang: to_lang});
        const result = await response.json();
        if (!response.ok) {
            offcanvasContentEl.innerHTML = `<p class="text-muted">${result.message}</p>`;
            return;
        }
        displayWordDefinition(offcanvasTitleEl, offcanvasContentEl, result.data);
    } catch (error) {
        offcanvasContentEl.innerHTML = `<p class="text-muted">Get definition failed, please try again</p>`;
    }
}

function displayWordDefinition(offcanvasTitleEl, contentDiv, data) {
    offcanvasTitleEl.innerHTML = `${data.word}`;

    const pronunciationSection = document.createElement('div');
    data.pronunciations.forEach(pronunciation => {
        if (pronunciation.hasAudio) {
            const button = document.createElement('button');
            button.classList.add('btn', 'btn-outline-secondary', 'me-2', 'btn-sm', 'mb-2');
            button.innerHTML = `${pronunciation.accent} ${pronunciation.pronunciation} ၊၊||၊`;
            button.onclick = () => speechWord(pronunciation.id);
            pronunciationSection.appendChild(button);
        }
    });
    contentDiv.appendChild(pronunciationSection);

    // Group translations by posTag
    const groupedTranslations = data.translations.reduce((acc, {posTag, translation}) => {
        if (!acc[posTag]) {
            acc[posTag] = [];
        }
        acc[posTag].push(translation);
        return acc;
    }, {});

    // Render grouped translations
    Object.keys(groupedTranslations).forEach(posTag => {
        const groupSection = document.createElement('div');
        groupSection.innerHTML = `<p class="my-1"><span class="me-3 text-muted small">${posTag}.</span>${groupedTranslations[posTag].join(', ')}</p>`;
        contentDiv.appendChild(groupSection);
    });
}


function getQueryString(params) {
    return new URLSearchParams(params).toString();
}

async function httpGet(baseUrl, params) {
    return await fetch(`${baseUrl}?${getQueryString(params)}`, {"method": "GET"});
}

async function translateSentence(button, sourceType, sourceId, sentenceNo, offcanvasContentEl, toLang) {
    button.innerText = 'Translating...';
    button.disabled = true;
    try {
        const response = await httpGet(TRANSLATION_URL, {
            source_type: sourceType,
            source_id: sourceId,
            sentence_no: sentenceNo,
            to_lang: toLang,
        })
        const result = await response.json();
        if (!response.ok) {
            offcanvasContentEl.innerHTML = `<p class="text-muted">${result.message}</p>`;
            button.disabled = false;
            return;
        }

        offcanvasContentEl.innerHTML += '<div class="mt-3">' + result.data.translation + '</div>';
        button.innerText = 'Translated';
    } catch (error) {
        offcanvasContentEl.innerHTML = '<p class="text-muted">Translate failed, please try again</p>';
        button.disabled = false;
    }
}


function speechWord(pronunciationId) {
    const params = {id: pronunciationId};
    const audio = new Audio(`${PLAY_WORD_URL}?${getQueryString(params)}`);
    audio.play();
}


let currentAudio = null;

function speechSentence(sourceType, sourceId, sentenceNo, voice) {
    const params = {source_type: sourceType, source_id: sourceId, sentence_no: sentenceNo, voice: voice};
    const new_audio_url = `${PLAY_SENTENCE_URL}?${getQueryString(params)}`;
    const new_audio = new Audio(new_audio_url);

    // if current audio is empty, play new audio
    if (!currentAudio) {
        currentAudio = new_audio;
        currentAudio.play();
        return;
    }

    const currentSrc = currentAudio.src;
    // if current audio is same audio and playing, stop it
    if (currentSrc === new_audio_url && !currentAudio.paused) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        return;
    }

    // if current audio is same audio and not playing, play it audio
    if (currentSrc === new_audio_url && currentAudio.paused) {
        currentAudio.play();
        return;
    }

    // if current audio is different audio, stop current audio and play new audio
    if (currentSrc !== new_audio_url) {
        currentAudio.pause();
        currentAudio = new_audio;
        currentAudio.play();
    }
}

const createBtn = function(text) {
    const btn = document.createElement('button');
    btn.innerText = text;
    btn.classList.add("btn", "btn-sm", "btn-outline-secondary", "me-2");
    return btn;
}

const initSentenceTranslation = function (sourceType, sourceId) {
    const sentence_btn_els = ARTICLE_CONTENT_EL.getElementsByTagName("s");

    Array.from(sentence_btn_els).forEach(function (s) {
        s.addEventListener('click', function (event) {
            s.classList.add('clicked');
            var sentenceSpanEl = event.currentTarget.parentElement;
            var sentenceNo = event.currentTarget.innerText;

            var toLang = LANGUAGE_SELECT_EL.value;
            if (!toLang) {
                alert('Please select target language at top right');
                return;
            }

            offcanvasTitleEl.innerHTML = '';
            offcanvasContentEl.innerHTML = '';

            const titleDiv = document.createElement('div');
            titleDiv.classList.add('d-flex', 'justify-content-center');

            const translateBtn = createBtn('Translate');
            titleDiv.appendChild(translateBtn);

            const playMaleVoiceBtn = createBtn('Echo ၊၊|၊');
            titleDiv.appendChild(playMaleVoiceBtn);

            const playFemaleVoiceBtn = createBtn('Shimmer ၊၊|၊');
            titleDiv.appendChild(playFemaleVoiceBtn);

            offcanvasTitleEl.appendChild(titleDiv);

            offcanvasContentEl.innerHTML = sentenceSpanEl.innerHTML;
            OFFCANVAS_INSTANCE.show();

            translateBtn.addEventListener('click', async function () {
                await translateSentence(translateBtn, sourceType, sourceId, sentenceNo, offcanvasContentEl, toLang);
            });

            playMaleVoiceBtn.addEventListener('click', function () {
                speechSentence(sourceType, sourceId, sentenceNo, 'echo');
            });

            playFemaleVoiceBtn.addEventListener('click', function () {
                speechSentence(sourceType, sourceId, sentenceNo, 'shimmer');
            });
        });
    });
}


const initWordTranslation = function () {
    const word_els = ARTICLE_CONTENT_EL.getElementsByTagName('i');

    Array.from(word_els).forEach(function (w) {
        w.addEventListener('click', function () {
            var toLang = LANGUAGE_SELECT_EL.value;
            if (!toLang) {
                alert('Please select target language at top right');
                return;
            }

            offcanvasTitleEl.innerHTML = 'Searching...';
            offcanvasContentEl.innerHTML = '';
            OFFCANVAS_INSTANCE.show();
            searchDictionary(offcanvasTitleEl, offcanvasContentEl, this.innerText, toLang);
        });
    });
}

function batchAction(inputList, action) {
    Array.from(inputList).forEach(item => action(item));
}

function setCookie(name, value, days) {
    let expires = "";
    let expiredDays = days || 365;

    const date = new Date();
    date.setTime(date.getTime() + (expiredDays * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();

    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    const nameEQ = name + "=";
    const cookiesArray = document.cookie.split(';');
    for (let i = 0; i < cookiesArray.length; i++) {
        let cookie = cookiesArray[i];
        while (cookie.charAt(0) === ' ') cookie = cookie.substring(1, cookie.length);
        if (cookie.indexOf(nameEQ) === 0) return cookie.substring(nameEQ.length, cookie.length);
    }
    return null;
}

function initFontAndDarkButtons() {
    // Button elements
    const decreaseFontBtn = document.getElementById('decreaseFont');
    const increaseFontBtn = document.getElementById('increaseFont');
    const toggleDarkModeBtn = document.getElementById('toggleDarkMode');

    // Decrease font size
    decreaseFontBtn.addEventListener('click', () => {
        let currentSize = parseFloat(getComputedStyle(document.body).fontSize);
        let newSize = currentSize - 1;
        document.body.style.fontSize = newSize + 'px';
        setCookie('fontSize', newSize + 'px');
    });

    // Increase font size
    increaseFontBtn.addEventListener('click', () => {
        let currentSize = parseFloat(getComputedStyle(document.body).fontSize);
        let newSize = currentSize + 1;
        document.body.style.fontSize = newSize + 'px';
        setCookie('fontSize', newSize + 'px');
    });

    // Toggle dark mode
    toggleDarkModeBtn.addEventListener('click', () => {
        document.body.classList.toggle('bg-dark');
        document.body.classList.toggle('text-light');
        darkMode = document.body.classList.contains('bg-dark') ? 'dark' : 'light';
        setCookie('darkMode', darkMode);
    });
}

function initLanguageSelection() {
    const languageSelector = document.getElementById('language-selector');

    languageSelector.addEventListener('change', () => {
        setCookie('language', languageSelector.value);
    });
}

function saveReadingProgress(bookSlug, chapterNo, sentenceId) {
    const readingProgress = {
        chapterNo: chapterNo,
        sentenceId: sentenceId,
    };
    localStorage.setItem(`bookReadingProgress_${bookSlug}`, JSON.stringify(readingProgress));
}

function getReadingProgress(bookSlug) {
    return localStorage.getItem(`bookReadingProgress_${bookSlug}`);
}

function loadReadingProgressToButton(buttonSelector) {
    var readButtonEls = document.querySelectorAll(buttonSelector);
    Array.from(readButtonEls).forEach(buttonEl => {
        const bookSlug = buttonEl.dataset.bookSlug;
        const storedProgress = getReadingProgress(bookSlug);

        if (storedProgress) {
            const {chapterNo, sentenceId} = JSON.parse(storedProgress);
            buttonEl.href = `/${bookSlug}/${chapterNo}.html#${sentenceId}`;
            buttonEl.innerText = `Continue Reading`;
        }
    });
}

function getFirstVisibleSentenceId() {
    // Get all <s> tags on the page
    const sTags = document.querySelectorAll('s');

    // Loop through the <s> tags to find the first visible one
    for (let sTag of sTags) {
        const rect = sTag.getBoundingClientRect();

        // Check if the element is in the visible window (partially or fully)
        if (rect.top >= 0 && rect.bottom <= window.innerHeight) {
            // Return the id of the first visible <s> tag
            return sTag.id;
        }
    }

    return 1;
}


function initStripePayment(stripeInstance) {
    var buyBtns = document.getElementsByClassName('buy');
    for (var i = 0; i < buyBtns.length; i++) {
        buyBtns[i].addEventListener("click", (e) => {
            e.preventDefault();
            var button = e.currentTarget;
            button.disabled = true;

            var data = {
                price_id: e.currentTarget.getAttribute("data-price-id"),
            }

            fetch(CREATE_PAYMENT_URL, {
                body: JSON.stringify(data),
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
                .then((response) => {
                    if (!response.ok) {
                        alert('Failed to create payment, please try again');
                        throw new Error('Failed to create payment session');
                    }
                    return response.json();
                })
                .then((json) => {
                    return stripeInstance.redirectToCheckout({sessionId: json.data.sessionId})
                })
                .then((res) => {
                    console.log(res);
                }).finally(() => button.disabled = false);
        });
    }
}