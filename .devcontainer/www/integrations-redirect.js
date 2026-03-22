class IntegrationsPanel extends HTMLElement {
  connectedCallback() {
    window.location.replace("/config/integrations");
  }
}
customElements.define("integrations-panel", IntegrationsPanel);
