export const helpHttp = () => {
  const customFetch = (endpoint, options) => {
    const defaultHeader = {
      accept: "application/json",
    };
    const controller = new AbortController();
    options.signal = controller.signal;
    options.method = options.method || "GET";
    options.headers = options.headers
      ? { ...defaultHeader, ...options.headers }
      : defaultHeader;
    options.body = JSON.stringify(options.body) || false;
    if (!options.body) delete options.body;
    setTimeout(() => {
      controller.abort();
    }, 5000);
    return fetch(endpoint, options)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Network response was not ok");
        }
        return res.json();
      })
      .catch((error) => {
        // Aquí manejas el error de red
        console.error("Error de red:", error);
        return Promise.reject({
          err: true,
          status: "00",
          statusText: "Error de red",
        });
      });
  };

  const get = (url, options = {}) => {
    return customFetch(url, options);
  };
  const post = (url, options = {}) => {
    options.method = "POST";
    return customFetch(url, options);
  };
  const put = (url, options = {}) => {
    options.method = "PUT";
    return customFetch(url, options);
  };
  const del = (url, options = {}) => {
    options.method = "DELETE";
    return customFetch(url, options);
  };

  return { get, post, put, del };
};
