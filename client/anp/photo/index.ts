import angular from 'angular';
import {reactToAngular1} from 'superdesk-ui-framework';
import SearchPanel from './SearchPanel';

export default angular.module('anp.photo', [
])
    .component('anpSearchPanel', reactToAngular1(SearchPanel, ['params', 'scope']))
    .run(['$templateCache', ($templateCache) => {
        $templateCache.put(
            'search-panel-anp.html',
            require('./views/search-panel-anp.html'),
        );
    }])
;
