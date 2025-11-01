/** @odoo-module **/

import { registry } from '@web/core/registry'
import { useService } from '@web/core/utils/hooks'
import { listView } from '@web/views/list/list_view'
import { ListController } from '@web/views/list/list_controller'

class circulationListController extends ListController{
    setup(){
        super.setup()
        this.action = useService("action")
    }
    async OpenGuestView() {
        await this.action.doAction({
            type: "ir.actions.act_window",
            name: "Copy Challan",
            res_model: "copy.challan.entry.wizard",
            views: [[false, "form"]],
            target: "new",
            context: {
//                default_type: 'guest',
//                default_flag: true
            },
        });
    }
    async UpdateChallanView() {
        await this.action.doAction({
            type: "ir.actions.act_window",
            name: "Lunch Order",
            res_model: "update.challan.entry.wizard",
            views: [[false, "form"]],
            target: "new",
            context: {
//                default_type: 'others',
//                default_flag: true
            },
        });
    }

}

export const circulationListView = {
    ...listView,
    Controller:circulationListController,
    buttonTemplate: "circulation.open_wiz_copy_challan.Buttons",

}

registry.category("views").add('circulation_list_view',circulationListView)