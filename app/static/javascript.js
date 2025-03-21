(function(win, doc) {
    'use strict';

    // Configuração do Piii.js com grupos menores de palavras
    const palavroes = [
        // Grupo 1 - Palavrões básicos
        ['merda', 'bosta', 'porra', 'caralho', 'buceta', 'puta', 'viado', 'cu'],
        
        // Grupo 2 - Variações e derivados
        ['babaca', 'otario', 'idiota', 'imbecil', 'burro', 'cuzao', 'fdp', 'puto'],
                    
        // Grupo 3 - Termos ofensivos
        ['gay', 'veado', 'bicha', 'boiola', 'sapatao', 'lesbica'],
        
        // Grupo 4 - Outros termos
        ['penis', 'vagina', 'xota', 'xana', 'bunda', 'rola', 'piroca'],

        //Grupo 5 - Termos utilizados durante testes
        ['Cacetoide', 'fodidinho']

    ];

    const piii = new Piii({
        filters: palavroes,
        aliases: {
            a: ['@', '4', 'á', 'à', 'ã', 'â'],
            e: ['3', 'é', 'ê'],
            i: ['1', 'í'],
            o: ['0', 'ó', 'õ', 'ô', 'u'],
            u: ['v', 'ú', 'ü']
        },
        censor: function(str) {
            return '*'.repeat(str.length); // Censura adaptativa ao tamanho da palavra
        },
        cleaner: function(str) {
            // Remove acentos e caracteres especiais
            return str.normalize('NFD')
                     .replace(/[\u0300-\u036f]/g, '')
                     .toLowerCase();
        }
    });

    // Função para filtrar palavrões
    function filtrarPalavroes(texto) {
        if (!texto) return texto;
        
        try {
            console.log('Texto original:', texto);
            let textoFiltrado = texto;
            
            // Filtra cada grupo separadamente
            palavroes.forEach(grupo => {
                const piiiGrupo = new Piii({
                    filters: [grupo],
                    aliases: piii._aliases,
                    censor: piii._censor,
                    cleaner: piii._cleaner
                });
                textoFiltrado = piiiGrupo.filter(textoFiltrado);
            });
            
            console.log('Texto filtrado:', textoFiltrado);
            return textoFiltrado;
        } catch (error) {
            console.error('Erro ao filtrar:', error);
            return texto;
        }
    }

    // Ajax do form
    if (doc.querySelector('#form')) {
        let form = doc.querySelector('#form');
        function sendForm(event) {
            event.preventDefault();
            let data = new FormData(form);
            
            try {
                // Filtra a mensagem antes de enviar
                let mensagem = data.get('mensagem');
                if (mensagem) {
                    let mensagemFiltrada = filtrarPalavroes(mensagem);
                    data.set('mensagem', mensagemFiltrada);
                }

                let ajax = new XMLHttpRequest();
                let token = doc.querySelector('input[name="csrfmiddlewaretoken"]').value;

                ajax.open('POST', form.action);
                ajax.setRequestHeader('X-CSRFToken', token);
                ajax.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

                ajax.onreadystatechange = function() {
                    if (ajax.readyState === 4) {
                        if (ajax.status === 200) {
                            let result = doc.querySelector('#result');
                            if (result) {
                                result.innerHTML = 'Mensagem enviada com sucesso!';
                                result.classList.add('alert');
                                result.classList.add('alert-success');

                                form.reset();

                                setTimeout(function() {
                                    window.location.href = '/mural';
                                }, 2000);
                            }
                        } else {
                            console.error('Erro ao enviar mensagem:', ajax.status);
                        }
                    }
                }

                ajax.onerror = function() {
                    console.error('Erro na requisição AJAX');
                };

                ajax.send(data);
            } catch (error) {
                console.error('Erro ao processar formulário:', error);
            }
        }
        form.addEventListener('submit', sendForm, false);
    }
})(window, document);