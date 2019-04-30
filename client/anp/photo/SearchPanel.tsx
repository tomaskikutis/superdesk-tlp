import React from 'react';
import {gettext} from 'superdesk-core/scripts/core/utils';

interface ISearchParams {
    reference: string;
    filename: string;
    firstdate: string;
    orientation: string;
};

interface IProps {
    params: ISearchParams;
}

interface IState extends Partial<ISearchParams> {}

const ORIENTATION = [
    {'id': '0', 'label': gettext('any')},
    {'id': '1', 'label': gettext('landscape')},
    {'id': '2', 'label': gettext('portrait')},
    {'id': '3', 'label': gettext('square')},
    {'id': '4', 'label': gettext('panoramic')},
];

const FIELDS = [
    {key: 'reference', label: gettext('Reference'), type: 'text'},
    {key: 'filename', label: gettext('File name'), type: 'text'},
    {key: 'orientation', label: gettext('Orientation'), type: 'radio', options: ORIENTATION},
    {key: 'firstdate', label: gettext('First date'), type: 'date'},
];

/**
 * This component updates props.params, using PureComponent to avoid re-rendering on such change.
 */
export default class SearchPanel extends React.PureComponent<IProps, IState> {

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
                    {field.type === 'radio' ? (
                        field.options.map((option, index) => (
                        <label key={option.id} className="search-label">
                            <input type="radio" name="orientation"
                                value={option.id}
                                onChange={() => this.onChange(field.key, option.id)}
                                checked={this.state[field.key] ? option.id === this.state[field.key] : index === 0}
                            />
                            {option.label}
                        </label>
                        ))
                    ) : (
                    <input type={field.type} name={field.key} onChange={(e) => this.onChange(field.key, e.target.value)} value={this.state[field.key]} />
                    )}
                </div>
                ))}
            </fieldset>
        );
    }
}