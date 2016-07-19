const orderCall = (() => {
  const DOM = {
    $phone: $('#back-call-phone'),
    $callModal: $('#back-call-modal'),
    $closeModal: $('.js-backcall-close'),
    $orderButton: $('.js-send-backcall'),
    $successTag: $('.js-backcall-success'),
    $timeText: $('.js-backcall-time'),
    $timeTag: $('.js-select-time'),
    $timeToCall: $('#back-call-time'),
  };

  const init = () => {
    setUpListeners();
  };

  const setUpListeners = () => {
    mediator.subscribe('onBackCallSend', showSuccessModal);

    DOM.$orderButton.on('click', orderCall);
    DOM.$timeTag.on('change', storeBackcallTime.bind(this));
    DOM.$callModal.on('hidden.bs.modal', resetErrorClass);
  };

  const orderCall = () => {
    const phone = DOM.$phone.val();
    const time = DOM.$timeToCall.val();
    const url = location.href;

    if (!validator.isPhoneValid(phone)) {
      DOM.$phone
        .addClass('shake animated')
        .closest('.form-group').addClass('has-error');
      return;
    }

    server.sendOrderCall(phone, time, url)
      .then(() => {
        DOM.$timeText.text(DOM.$timeTag.val());
        mediator.publish('onBackCallSend');
      });
  };

  const showSuccessModal = () => {
    DOM.$orderButton.addClass('hidden');
    DOM.$closeModal.removeClass('hidden');
    DOM.$successTag
      .removeClass('hidden')
      .siblings().addClass('hidden');
  };

  const resetErrorClass = () => {
    DOM.$phone
      .removeClass('shake animated')
      .closest('.form-group').removeClass('has-error');
  };

  const storeBackcallTime = (selectedOption) => {
    const selectedTime = $(selectedOption.target).find(':selected').data('time');

    localStorage.setItem(configs.LABELS.callTime, selectedTime);
  };

  init();
})();