function renderEmbeddedFigures() {
    document.querySelectorAll('script[type="application/json"][id$="-data"]').forEach(function (el) {
        const targetId = el.id.slice(0, -('-data'.length));
        const target = document.getElementById(targetId);
        if (!target) return;
        const spec = JSON.parse(el.textContent);
        Plotly.newPlot(target, spec.data, spec.layout, { responsive: true });
    });
}

document.addEventListener('DOMContentLoaded', renderEmbeddedFigures);

document.addEventListener('shown.bs.tab', function (evt) {
    const target = document.querySelector(evt.target.getAttribute('data-bs-target'));
    if (!target) return;
    target.querySelectorAll('[id]').forEach(function (el) {
        if (el._fullLayout) Plotly.Plots.resize(el);
    });
});

document.body.addEventListener('htmx:afterRequest', function (evt) {
    const targetId = evt.detail.elt.dataset.plotlyTarget;
    if (!targetId) return;
    const target = document.getElementById(targetId);
    if (!target || !evt.detail.successful) return;
    const spec = JSON.parse(evt.detail.xhr.response);
    Plotly.react(target, spec.data, spec.layout);
});
