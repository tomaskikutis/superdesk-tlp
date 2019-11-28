import angular from 'angular';
import { reactToAngular1 } from 'superdesk-ui-framework';
import TalpaVideoSearchPanel from './talpaVideoSearchPanel';

export default angular.module('anp.talpaVideo', [])
  .component('talpaVideoSearchPanel', reactToAngular1(TalpaVideoSearchPanel, ['params', 'scope']))
  .run(['$templateCache', ($templateCache) => {
    $templateCache.put(
      'search-panel-talpa_video.html',
      require('./views/search-panel.html'),
    );
  }]);
