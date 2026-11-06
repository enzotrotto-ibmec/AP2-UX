;(function($){
    "use strict"
    var nav_offset_top = $('.header_area').height()+50; 
    /*-------------------------------------------------------------------------------
	  Navbar 
	-------------------------------------------------------------------------------*/

	//* Navbar Fixed  
    function navbarFixed(){
        if ( $('.header_area').length ){ 
            $(window).scroll(function() {
                var scroll = $(window).scrollTop();   
                if (scroll >= nav_offset_top ) {
                    $(".header_area").addClass("navbar_fixed");
                } else {
                    $(".header_area").removeClass("navbar_fixed");
                }
            });
        };
    };
    navbarFixed();
    
    function testimonialSlider(){
        if ( $('.testimonial_slider').length ){
            $('.testimonial_slider').owlCarousel({
                loop:true,
                margin: 30,
                items: 2,
                nav:false,
                autoplay: true,
                dots: true,
                smartSpeed: 1500,
                responsiveClass: true,
                responsive: {
                    0: {
                        items: 1,
                    },
                    768: {
                        items: 2,
                    },
                }
            })
        }
    }
    testimonialSlider();
    
    //------- Mailchimp js --------//  

    function mailChimp(){
        $('#mc_embed_signup').find('form').ajaxChimp();
    }
    mailChimp();
    
    /* ===== Parallax Effect===== */
	
	function parallaxEffect() {
    	$('.bg-parallax').parallax();
	}
	parallaxEffect();
    
    
    $('select').niceSelect();

    /*----------------------------------------------------*/
    /*  Seletor de data e hora em portugues (DD/MM/AAAA hh:mm)
    /*----------------------------------------------------*/
    $.fn.datetimepicker.dates['pt-BR'] = {
        days: ["domingo", "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"],
        daysShort: ["dom", "seg", "ter", "qua", "qui", "sex", "sáb", "dom"],
        daysMin: ["do", "se", "te", "qa", "qi", "sx", "sá", "do"],
        months: ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"],
        monthsShort: ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"],
        today: "Hoje",
        suffix: [],
        meridiem: []
    };
    $('#datetimepicker11,#datetimepicker1').datetimepicker({
        format: 'dd/mm/yyyy hh:ii',
        language: 'pt-BR',
        autoclose: true,
        startDate: new Date(),
        minuteStep: 30,
        daysOfWeekDisabled: [1]   // fechado as segundas-feiras
    });

    /*----------------------------------------------------*/
    /*  Reserva de mesa -> mensagem pronta no WhatsApp (sem servidor)
    /*----------------------------------------------------*/
    // Numero do restaurante: so digitos com DDI+DDD, ex.: "5521999999999".
    // Vazio = o WhatsApp abre com a mensagem pronta e a pessoa escolhe o contato.
    var WHATSAPP_RESTAURANTE = "";

    function avisoReserva(texto, erro){
        var $aviso = $('#reserva-aviso');
        if (!$aviso.length){
            $aviso = $('<div id="reserva-aviso" class="reserva_aviso" role="status" aria-live="polite"></div>').appendTo('body');
        }
        $aviso.stop(true, true).removeClass('erro ok').addClass(erro ? 'erro' : 'ok').text(texto).fadeIn(200);
        clearTimeout($aviso.data('t'));
        $aviso.data('t', setTimeout(function(){ $aviso.fadeOut(300); }, 6000));
    }

    function reservaWhatsApp(){
        $('.book_now_btn').on('click', function(e){
            e.preventDefault();
            var $box = $(this).closest('.boking_table');
            var data = $.trim($box.find('input[name="data"]').val());
            var alternativa = $.trim($box.find('input[name="data_alternativa"]').val());
            var escolha = function(nome){
                var $s = $box.find('select[name="' + nome + '"]');
                return $s.val() ? $.trim($s.find('option:selected').text()) : '';
            };
            var adultos = escolha('adultos'), criancas = escolha('criancas'), ambiente = escolha('ambiente');

            var faltam = [];
            if (!data) faltam.push('data e horário');
            if (!adultos) faltam.push('número de adultos');
            if (!ambiente) faltam.push('ambiente');
            if (faltam.length){
                avisoReserva('Para reservar, informe: ' + faltam.join(', ') + '.', true);
                return;
            }

            // funcionamento: terca a domingo, das 12h as 23h (a segunda ja e bloqueada no seletor)
            var foraDoHorario = function(txt){
                var m = /(\d{2}):(\d{2})$/.exec(txt || '');
                return m ? (+m[1] < 12 || +m[1] >= 23) : false;
            };
            if (foraDoHorario(data) || foraDoHorario(alternativa)){
                avisoReserva('Atendemos de terça a domingo, das 12h às 23h. Escolha um horário nesse intervalo.', true);
                return;
            }

            var linhas = ['Olá! Gostaria de reservar uma mesa no Ristorantti Cucina Italiana.',
                          '',
                          'Data e horário: ' + data];
            if (alternativa) linhas.push('Horário alternativo: ' + alternativa);
            linhas.push('Adultos: ' + adultos);
            if (criancas) linhas.push('Crianças: ' + criancas);
            linhas.push('Ambiente: ' + ambiente, '', 'Aguardo a confirmação. Obrigado!');

            var url = 'https://wa.me/' + WHATSAPP_RESTAURANTE + '?text=' + encodeURIComponent(linhas.join('\n'));
            window.open(url, '_blank', 'noopener');
            avisoReserva('Abrimos o WhatsApp com a sua reserva pronta. Envie a mensagem para confirmar!', false);
        });
    }
    reservaWhatsApp();
    
     /*---------gallery isotope js-----------*/
    function galleryMasonry(){
        if ( $('#gallery').length ){
            $('#gallery').imagesLoaded( function() {
              // images have loaded
                // Activate isotope in container
                $("#gallery").isotope({
                    itemSelector: ".gallery_item",
                    layoutMode: 'masonry',
                    animationOptions: {
                        duration: 750,
                        easing: 'linear'
                    }
                });
            })
        }
    }
    galleryMasonry();
	
	/*----------------------------------------------------*/
    /*  Simple LightBox js
    /*----------------------------------------------------*/
    $('.imageGallery1 .light').simpleLightbox();
    
    /*----------------------------------------------------*/
    /*  Google map js
    /*----------------------------------------------------*/
    
    if ( $('#mapBox').length ){
        var $lat = $('#mapBox').data('lat');
        var $lon = $('#mapBox').data('lon');
        var $zoom = $('#mapBox').data('zoom');
        var $marker = $('#mapBox').data('marker');
        var $info = $('#mapBox').data('info');
        var $markerLat = $('#mapBox').data('mlat');
        var $markerLon = $('#mapBox').data('mlon');
        var map = new GMaps({
        el: '#mapBox',
        lat: $lat,
        lng: $lon,
        scrollwheel: false,
        scaleControl: true,
        streetViewControl: false,
        panControl: true,
        disableDoubleClickZoom: true,
        mapTypeControl: false,
        zoom: $zoom,
            styles: [
                {
                    "featureType": "water",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#dcdfe6"
                        }
                    ]
                },
                {
                    "featureType": "transit",
                    "stylers": [
                        {
                            "color": "#808080"
                        },
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "geometry.stroke",
                    "stylers": [
                        {
                            "visibility": "on"
                        },
                        {
                            "color": "#dcdfe6"
                        }
                    ]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                },
                {
                    "featureType": "road.local",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "visibility": "on"
                        },
                        {
                            "color": "#ffffff"
                        },
                        {
                            "weight": 1.8
                        }
                    ]
                },
                {
                    "featureType": "road.local",
                    "elementType": "geometry.stroke",
                    "stylers": [
                        {
                            "color": "#d7d7d7"
                        }
                    ]
                },
                {
                    "featureType": "poi",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "visibility": "on"
                        },
                        {
                            "color": "#ebebeb"
                        }
                    ]
                },
                {
                    "featureType": "administrative",
                    "elementType": "geometry",
                    "stylers": [
                        {
                            "color": "#a7a7a7"
                        }
                    ]
                },
                {
                    "featureType": "road.arterial",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                },
                {
                    "featureType": "road.arterial",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                },
                {
                    "featureType": "landscape",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "visibility": "on"
                        },
                        {
                            "color": "#efefef"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "labels.text.fill",
                    "stylers": [
                        {
                            "color": "#696969"
                        }
                    ]
                },
                {
                    "featureType": "administrative",
                    "elementType": "labels.text.fill",
                    "stylers": [
                        {
                            "visibility": "on"
                        },
                        {
                            "color": "#737373"
                        }
                    ]
                },
                {
                    "featureType": "poi",
                    "elementType": "labels.icon",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "poi",
                    "elementType": "labels",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "road.arterial",
                    "elementType": "geometry.stroke",
                    "stylers": [
                        {
                            "color": "#d6d6d6"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "labels.icon",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {},
                {
                    "featureType": "poi",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#dadada"
                        }
                    ]
                }
            ]
        });
    }

})(jQuery)