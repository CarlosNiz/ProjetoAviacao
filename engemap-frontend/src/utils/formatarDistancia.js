function formatarDistancia(metros) {
  if (metros < 1000) {
    return `${metros.toFixed(0)} m`;
  }
  return `${(metros / 1000).toFixed(2)} km`;
}

export default formatarDistancia;