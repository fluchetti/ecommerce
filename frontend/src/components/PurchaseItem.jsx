import React from "react";

const PurchaseItem = ({ purchase }) => {
  return (
    <div className="card p-3 m-2">
      <div className="card-header">
        <h5 className="card-title">Detalle de compra</h5>
        <p>Identificador de compra: {purchase.id} </p>
        <p style={{ fontWeight: "bold" }}>
          Status: {purchase.is_delivered ? "Entregada" : "En preparacion"}{" "}
        </p>
      </div>
      <div className="card-body">
        <h5>Productos</h5>
        <ul className="list-group list-group-flush">
          {purchase.cart_items.map((item, index) => (
            <li className="list-group-item" key={index}>
              <div>Producto: {item.product}</div>
              <div>Cantidad: {item.quantity}</div>
              <div>Precio: ${item.price}</div>
            </li>
          ))}
        </ul>
        <div className="card-footer">
          <div>Total: ${purchase.total_price}</div>
          <div>Fecha de compra: {purchase.created}</div>
        </div>
      </div>
    </div>
  );
};

export default PurchaseItem;
