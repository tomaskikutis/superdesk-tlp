import React from 'react';
import { gettext } from 'superdesk-core/scripts/core/utils';


interface ISearchParams {
  // searchParam: string;
}


interface IProps {
  params: ISearchParams;
}


interface IState extends Partial<ISearchParams> {
}


const FIELDS = [
  // {key: 'searchParam', label: gettext('Search'), type: 'text'},
];


/**
 * This component updates props.params, using PureComponent to avoid re-rendering on such change.
 */
export default class TalpaVideoSearchPanel extends React.PureComponent<IProps, IState> {

  readonly state = Object.assign({}, this.props.params);

  onChange(key: string, val: string) {
    const update: IState = {
      [key]: val,
    };

    this.setState(update, () => {
      Object.assign(this.props.params, this.state);
    });
  }

  render() {
    return (
      <fieldset>
        {FIELDS.map((field) => (
          <div key={field.key} className="field">
            <label className="search-label">{field.label}</label>
            <input type={field.type}
                   name={field.key} onChange={(e) => this.onChange(field.key, e.target.value)}
                   value={this.state[field.key]}
            />
          </div>
        ))}
      </fieldset>
    );
  }
}