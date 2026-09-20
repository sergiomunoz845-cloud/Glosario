/* ========================================================================
   Glosario de IA — interacción del navegador
   1. Filtrado en vivo (sin recargar la página). Si el visitante tiene
      JavaScript desactivado, el formulario sigue funcionando contra Flask.
   2. Cuestionario del modo estudio.
   ======================================================================== */

(function () {
  "use strict";

  var GLOSARIO = [];
  var datos = document.getElementById("datos-glosario");
  if (datos) {
    try {
      GLOSARIO = JSON.parse(datos.textContent);
    } catch (error) {
      GLOSARIO = [];
    }
  }

  var campo = document.getElementById("q");
  var formulario = campo ? campo.form : null;
  var fichas = Array.prototype.slice.call(document.querySelectorAll(".termino"));
  var conteo = document.getElementById("conteo");
  var vacio = document.getElementById("vacio");
  var filtros = Array.prototype.slice.call(document.querySelectorAll(".filtro"));
  var categoriaActiva = "";

  /* Quita acentos y pasa a minúsculas para buscar sin tildes. */
  function normalizar(texto) {
    return texto
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function aplicarFiltros() {
    if (!fichas.length) return;

    var clave = normalizar(campo ? campo.value.trim() : "");
    var visibles = 0;

    fichas.forEach(function (ficha) {
      var coincideTexto = !clave || normalizar(ficha.dataset.busqueda || "").indexOf(clave) !== -1;
      var coincideCategoria = !categoriaActiva || ficha.dataset.categoria === categoriaActiva;
      var visible = coincideTexto && coincideCategoria;

      ficha.classList.toggle("oculto", !visible);
      if (visible) visibles += 1;
    });

    if (conteo) {
      conteo.textContent = clave || categoriaActiva
        ? visibles + " de " + fichas.length + " términos"
        : fichas.length + " términos en " + contarCategorias() + " categorías";
    }
    if (vacio) vacio.classList.toggle("oculto", visibles !== 0);

    actualizarDireccion(clave ? campo.value.trim() : "", categoriaActiva);
  }

  function contarCategorias() {
    var vistas = [];
    fichas.forEach(function (ficha) {
      if (vistas.indexOf(ficha.dataset.categoria) === -1) vistas.push(ficha.dataset.categoria);
    });
    return vistas.length;
  }

  /* Mantiene la dirección del navegador sincronizada para poder compartirla. */
  function actualizarDireccion(consulta, categoria) {
    if (!window.history || !window.history.replaceState) return;
    var parametros = new URLSearchParams();
    if (consulta) parametros.set("q", consulta);
    if (categoria) parametros.set("categoria", categoria);
    var cadena = parametros.toString();
    window.history.replaceState(null, "", cadena ? "?" + cadena : window.location.pathname);
  }

  if (formulario) {
    formulario.addEventListener("submit", function (evento) {
      evento.preventDefault();
      aplicarFiltros();
    });
  }
  if (campo) campo.addEventListener("input", aplicarFiltros);

  filtros.forEach(function (filtro) {
    filtro.addEventListener("click", function (evento) {
      evento.preventDefault();
      categoriaActiva = filtro.dataset.categoria || "";
      filtros.forEach(function (otro) {
        otro.classList.toggle("activo", otro === filtro);
      });
      aplicarFiltros();
    });
  });

  /* Estado inicial tomado de la dirección (?q=...&categoria=...). */
  (function estadoInicial() {
    var parametros = new URLSearchParams(window.location.search);
    var consulta = parametros.get("q") || "";
    var categoria = parametros.get("categoria") || "";

    if (campo && consulta) campo.value = consulta;
    if (categoria) {
      categoriaActiva = categoria;
      filtros.forEach(function (filtro) {
        filtro.classList.toggle("activo", (filtro.dataset.categoria || "") === categoria);
      });
    }
    if (consulta || categoria) aplicarFiltros();
  })();

  /* ---------------------------------------------------------------------
     Modo estudio
     --------------------------------------------------------------------- */

  var boton = document.getElementById("iniciar-estudio");
  var contenedor = document.getElementById("cuestionario");
  var marcador = document.getElementById("marcador");
  var aciertos = 0;
  var respondidas = 0;
  var TOTAL_PREGUNTAS = 5;

  function revolver(lista) {
    var copia = lista.slice();
    for (var i = copia.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var temporal = copia[i];
      copia[i] = copia[j];
      copia[j] = temporal;
    }
    return copia;
  }

  function actualizarMarcador() {
    if (!marcador) return;
    marcador.classList.remove("oculto");
    marcador.textContent = "Aciertos: " + aciertos + " de " + respondidas +
      " (" + TOTAL_PREGUNTAS + " preguntas en total)";
  }

  function crearPregunta(entrada, numero) {
    var distractores = revolver(GLOSARIO.filter(function (otro) {
      return otro.id !== entrada.id;
    })).slice(0, 3);
    var opciones = revolver(distractores.concat([entrada]));

    var bloque = document.createElement("div");
    bloque.className = "pregunta";

    var texto = document.createElement("p");
    texto.className = "texto";
    texto.textContent = numero + ". " + entrada.definicion;
    bloque.appendChild(texto);

    var grupo = document.createElement("div");
    grupo.className = "opciones";

    opciones.forEach(function (opcion) {
      var boton = document.createElement("button");
      boton.type = "button";
      boton.className = "opcion";
      boton.textContent = opcion.termino;
      boton.addEventListener("click", function () {
        var botones = grupo.querySelectorAll(".opcion");
        Array.prototype.forEach.call(botones, function (otro) {
          otro.disabled = true;
        });
        respondidas += 1;
        if (opcion.id === entrada.id) {
          aciertos += 1;
          boton.classList.add("correcta");
        } else {
          boton.classList.add("incorrecta");
          Array.prototype.forEach.call(botones, function (otro) {
            if (otro.textContent === entrada.termino) otro.classList.add("correcta");
          });
        }
        actualizarMarcador();
      });
      grupo.appendChild(boton);
    });

    bloque.appendChild(grupo);
    return bloque;
  }

  if (boton && contenedor) {
    boton.addEventListener("click", function () {
      if (GLOSARIO.length < 4) return;
      aciertos = 0;
      respondidas = 0;
      contenedor.innerHTML = "";
      contenedor.classList.remove("oculto");

      revolver(GLOSARIO).slice(0, TOTAL_PREGUNTAS).forEach(function (entrada, indice) {
        contenedor.appendChild(crearPregunta(entrada, indice + 1));
      });

      boton.textContent = "Generar otras preguntas";
      if (marcador) {
        marcador.classList.remove("oculto");
        marcador.textContent = "Aciertos: 0 de 0 (" + TOTAL_PREGUNTAS + " preguntas en total)";
      }
    });
  }
})();
