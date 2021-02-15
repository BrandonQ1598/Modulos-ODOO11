# -*- coding: utf-8 -*-


from odoo import models, fields, api


class StockState(models.Model):
    _inherit = "stock.warehouse"

    is_estate = fields.Boolean(string="Predio", default=False)
    #season_id = fields.Many2one("stock.state.season", string="Temporada")
    active = fields.Boolean(string="Activo", default=True)
    hectare = fields.Float(string="Hectáreas", default=0.00)

    @api.model
    def create(self, vals):
        res = super(StockState, self).create(vals)
        # Acceder a la ubicación vista
        location_obj = self.env['stock.location'].browse([vals.get('view_location_id')])
        picking_type_obj = self.env['stock.picking.type'].search([('warehouse_id', '=', res.id)])
        # Id de la ubicación vista
        location_view_id = int(vals.get('view_location_id'))
        # Ids de las demás ubicaciones considerando como base la vista
        location_ids = [location_view_id + 1, location_view_id + 2, location_view_id + 3, location_view_id + 4, location_view_id + 5]
        # Objeto de las ubicaciones a modificar la información
        sublocations_obj = self.env['stock.location'].browse(location_ids)
        # Modificación de ubicaciones stock.location
        if vals.get('is_estate'):
            location_obj.write({'is_estate': True})
            for loc in sublocations_obj:
                loc.write({'is_estate': True})
            # Modificación de Tipos de operación stock.picking.type
            for picking in picking_type_obj:
                picking.write({'is_estate': True})
        else:
            location_obj.write({'is_estate': False})
            for loc in sublocations_obj:
                loc.write({'is_estate': False})
            # Modificación de Tipos de operación stock.picking.type
            for picking in picking_type_obj:
                picking.write({'is_estate': False})
        return res



class StockEstateLocation(models.Model):
    _inherit = "stock.location"

    is_estate = fields.Boolean(string="Ubicación de Predio", default=False)


class StockEstateLocationType(models.Model):
    _inherit = "stock.picking.type"

    is_estate = fields.Boolean(string="Tipo ubicación predio", default=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: